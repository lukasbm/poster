import subprocess
import uuid
import os
import json


class JobManager:
    def __init__(self):
        self.callbacks = {
            'before_job_start': [],
            'before_run_start': [],
            'on_run_start': [],
            'on_run_end': [],
            'after_run_end': [],
            'after_job_end': [],
        }
        self.job_history = {}
        self.context = {}  # Shared context for callbacks

    def register_callback(self, event_name, callback):
        if event_name in self.callbacks:
            self.callbacks[event_name].append(callback)
        else:
            raise ValueError(f"Event '{event_name}' is not supported.")

    def run_job(self, script_path, config={}, rerun_job_id=None):
        if rerun_job_id is not None:
            config = self.load_previous_config(rerun_job_id)
        job_id = str(uuid.uuid4())
        config['job_id'] = job_id
        self.context['config'] = config
        self.context['script_path'] = script_path
        self.trigger_callbacks('before_job_start')

        self.setup_environment()
        self.trigger_callbacks('before_run_start')

        self.trigger_callbacks('on_run_start')
        self.execute_script()
        self.trigger_callbacks('on_run_end')

        self.trigger_callbacks('after_run_end')
        self.trigger_callbacks('after_job_end')

        self.save_job_history()

    def trigger_callbacks(self, event_name):
        for callback in self.callbacks[event_name]:
            callback(self.context)

    def setup_environment(self):
        config = self.context['config']
        # Configure environment variables, SLURM settings, etc.
        if config.get('use_slurm'):
            slurm_settings = config.get('slurm_settings', {})
            # Set SLURM environment variables
            for key, value in slurm_settings.items():
                os.environ[key] = str(value)

    def execute_script(self):
        config = self.context['config']
        script_path = self.context['script_path']
        if config.get('use_slurm'):
            # Submit the script using SLURM's sbatch command
            command = ['sbatch', script_path]
        else:
            # Run the script normally
            command = ['python', script_path]

        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        self.context['stdout'] = stdout.decode()
        self.context['stderr'] = stderr.decode()
        self.context['returncode'] = process.returncode

    def save_job_history(self):
        config = self.context['config']
        job_id = config['job_id']
        self.job_history[job_id] = self.context.copy()
        # Optionally save to disk
        with open(f'job_{job_id}.json', 'w') as f:
            json.dump(self.context, f)

    def load_previous_config(self, job_id):
        # Load from disk
        with open(f'job_{job_id}.json', 'r') as f:
            context = json.load(f)
        return context['config']
