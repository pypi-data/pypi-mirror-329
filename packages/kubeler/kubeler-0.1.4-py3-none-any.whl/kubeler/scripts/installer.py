import yaml, os, sys, subprocess, shutil, jinja2
from kubernetes import client, config as k8sconfig
from .models.kubeler import Kubeler
from .watchdog import watch_directory

tmp_dir = "/tmp/kubeler"
k8sconfig.load_kube_config()
v1 = client.CoreV1Api()

class Installer:
    def __init__(self, installer, kube_config, start_from, steps, excludes, watch):
        self.installer = installer
        self.kube_config = kube_config
        self.start_from = start_from
        self.kube_config = kube_config
        self.steps = steps
        self.excludes = excludes
        self.watch = watch

        # get the directory path of the installer and kube_config
        self.installer_dir_path = os.path.dirname(installer)
        self.kube_config_path = os.path.dirname(kube_config)

        # create tmp dir if not exists
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

    def install(self):
        kubeler = self.load_config()
        
        # process init
        init_cmd = kubeler.init.cmd
        for command in init_cmd:
            cmd = command.split()
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
            for line in process.stdout:
                print(line, end="")
                sys.stdout.flush()
            process.wait()

        # process steps
        steps = kubeler.group.steps
        for step in steps:
            # extract step information
            step_name = step.name
            dir = os.path.join(self.installer_dir_path, step.dir)
            files = step.files
            vars = step.vars

            # if files is not defined in installer.yaml, load all files in the directory
            if files == None:
                files = self.load_files_in_dir(dir)
                
            for file in files:
                file_path = os.path.join(dir, file)
                config_path = os.path.join(tmp_dir, file)

                # set execution dir. It will be in tmp folder if vars is defined
                execution_dir = dir
                if vars != None:
                    # copy files for execution
                    shutil.copy(file_path, config_path) 

                    # create dictionary of variables
                    vars_dict = {var.name: var.value for var in vars}
                    # using jinja, replace variables in file
                    with open(config_path, "r") as config_file:
                        template_content = config_file.read()
                        template = jinja2.Template(template_content)
                        rendered_yaml = template.render(vars_dict)

                        with open(config_path, "w") as config_file:
                            config_file.write(rendered_yaml)
                    
                    # update dir variable
                    execution_dir = tmp_dir
                
                # get commands defined in the file
                commands = self.load_file(file_path)
                self.execute(commands, execution_dir)

                # if config_path exists, restore the file
                if os.path.exists(config_path):
                    os.remove(config_path)

        if kubeler.group.watch.enabled == True and self.watch == "true":
            watch_directory(self, os.path.abspath(self.installer_dir_path), kubeler.group.watch.dir)

    def execute(self, commands, execution_dir):
        for command in commands:
            print("Executing command: ", command)
            cmd = command.split()
            process = subprocess.Popen(cmd, cwd=execution_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
            for line in process.stdout:
                print(line, end="")
                sys.stdout.flush()
            process.wait()

    # if there some files in the directory, load them
    def load_files_in_dir(self, dir):
        files = []
        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)):
                files.append(file)
        return files

    # load commands on each files    
    def load_file(self, file_path):
        commands = []
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("#cmd:"):
                    command = line.split(":", 1)[1].strip()
                    command = self.handle_helm_chart_idempotency(command)
                    commands.append(command)
                        
        return commands

    #  load the configuration file and parse to Kubeler model
    def load_config(self) -> Kubeler:
        data = self.open_config()
        kubeler = Kubeler(**data)

        # handle reference variables
        for step in kubeler.group.steps:
            if step.vars != None:
                for var in step.vars:
                    if var.value.startswith("ref."):
                        ref_var = var.value.split("ref.")[1]
                        ref_vars = ref_var.split(".")
                        step_name = ref_vars[0]
                        var_name = ref_vars[2]
                        for step in kubeler.group.steps:
                            if step.vars != None:
                                if (step.name == step_name):
                                    for ref in step.vars:
                                        if ref.name == var_name:
                                            var.value = ref.value

        # handle environment variables
        for step in kubeler.group.steps:
            if step.vars != None:
                for var in step.vars:
                    if var.value.startswith("env."):
                        env_var = var.value.split("env.")[1]
                        var.value = os.environ.get(env_var)

        # handle excludes
        if self.excludes != None:
            excludes = self.excludes.split(",")
            for exclude in excludes:
                for step in kubeler.group.steps:
                    if step.name == exclude:
                        kubeler.group.steps.remove(step)
        
        for step in kubeler.group.steps:
            if step.exclude == "yes" or step.exclude == True:
                kubeler.group.steps.remove(step)

        # handle start from step
        if self.start_from != None:
            start_from = self.start_from
            for step in kubeler.group.steps:
                if step.name == start_from:
                    kubeler.group.steps = kubeler.group.steps[kubeler.group.steps.index(step):]

        # handle only run specific steps
        if self.steps != None:
            steps = self.steps.split(",")
            for step in kubeler.group.steps[:]:
                if step.name not in steps:
                    kubeler.group.steps.remove(step)

        return kubeler

    # open the configuration file    
    def open_config(self):
        with open(self.installer, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                return data
            except yaml.YAMLError as exc:
                raise ValueError("Failed to load configuration")
            
    def is_helm_chart_installed(self, release_name, namespace="default"):
        secrets = v1.list_namespaced_secret(namespace).items
        for secret in secrets:
            labels = secret.metadata.labels or {}
            if labels.get("owner") == "helm" and labels.get("name") == release_name:
                return True
        return False
    
    def handle_helm_chart_idempotency(self, command):
        # check if it's helm from: #cmd: helm install ...
        if command.startswith("helm install"):
            # get namespace from some scenarios:
            # -n <namespace>
            # --namespace <namespace>
            # --namespace=<namespace>
            namespace = None
            if "-n" in command:
                namespace = command.split("-n")[1].split()[0]
            elif "--namespace" in command:
                namespace = command.split("--namespace")[1].split()[0]
            elif "--namespace=" in command:
                namespace = command.split("--namespace=")[1].split()[0]
            
            # get release name from: #cmd: helm install <release_name> ...
            # get after `helm install` or `helm upgrade`
            release_name = None
            if "install" in command:
                release_name = command.split("install")[1].split()[0]
            elif "upgrade" in command:
                release_name = command.split("upgrade")[1].split()[0]
            
            if namespace != None:
                if self.is_helm_chart_installed(release_name, namespace):
                    # remove --install and replace install with upgrade
                    command = command.replace("--install", "").replace("install", "upgrade")
            
        return command