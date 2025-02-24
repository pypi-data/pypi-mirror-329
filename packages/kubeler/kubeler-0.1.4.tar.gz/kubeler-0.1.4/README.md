# Kubeler

Simple Kubernetes Resources installer

Dependencies
- Python >= 3.12

# Installation

```
pip install kubeler
```

## Usage
```
kubeler install --installer=./examples/installer.yaml
```

## Configuration

You can use your existing K8s manifest files. For a simple setup, just add `cmd: [kubectl/helm command]` to your manifest file. For example, you can take a look at some examples in the `examples` directory.

```
#cmd: kubectl apply -f namespace.yaml
---
kind: Namespace
apiVersion: v1
metadata:
  name: staging
  labels:
    name: staging
---
```

Then, create an installer YAML file to define your K8s resources. For example:

```
init:
  cmd: 
    - apt update -y
    - apt upgrade

group:
  name: k8s
  steps:
    - name: cluster
      dir: ./cluster
    - name: cert-manager
      dir: ./cert
```

Please note that when you create `installer.yml`, Kubeler will execute commands in order. So, make sure to place dependent resources before any resources that rely on them.

If you have multiple files inside a directory and want to define the execution order, you can list your files in the desired sequence.

```
...
- name: argocd
    dir: ./tools/argocd
    files:
        - manifest.yaml
        - ingress.yaml
```

You can also use variables to dynamically insert values into your manifest file.

```
...
spec:
  ingressClassName: {{ ingress_class }}
  rules:
    - host: {{ host_url }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service: 
                name: argocd-server
                port: 
                  name: https
```

Then, define the variables in `installer.yaml`.

```
- name: argocd
    dir: ./tools/argocd
    files:
        - manifest.yaml
        - ingress.yaml
    vars:
        - name: ingress_class
          value: nginx
        - name: host_url
          value: argocd.example.com
```

You can also reference variables from a previous step using `ref.`.

```
- name: redis
    dir: ./tools/redis
    vars:
        - name: password
          value: Password01

- name: harbor
    dir: ./tools/harbor
    vars:
        - name: redis_password  
          value: ref.redis.vars.password
```

You can also reference variables from environment variables using `env.`. In addition, using `.env` file defined in the same directory with `installer.yaml` also works for this case.

```
- name: harbor
    dir: ./tools/harbor
    vars:
        - name: redis_password  
          value: env.REDIS_PASSWORD
```

### Attributes

- `name`: Name of the step.
- `dir`: Directory where the manifest files reside.
- `files`: List of files in the directory that will be executed in order.
- `vars`: Variables for dynamic values inside the manifest file.

## Options

There are some options available with installing Kubernetes Resources using Kubeler.

### Exclude Steps

Use attributes `exclude=yes` or argument `--excludes` if you want to skip some steps from execution

```
steps:
  - name: cluster
    dir: ./cluster
    exclude: yes
```

or 
```
--installer=./../examples/installer.yaml --excludes=argocd,redis
```

### Define starting point

Use argument `--start-from` if you want to execute steps from a certain point

```
--installer=./../examples/installer.yaml --start-from=argocd
```

## Execute only some steps

Use argument `--steps` if you want to only execute some steps and exclude the other

```
--installer=./../examples/installer.yaml --steps=argocd,redis
```

## Watching for file changes

Use the `--watch` argument to monitor a directory and automatically apply changes when they occur.

Update `installer.yaml` to set `watch` attribute

```
group:
  name: k8s
  watch:
    enabled: true
    dir: 
      - ./applications
      - ./cluster
```

and then, run

```
kubeler install --installer=./examples/installer.yaml --watch=true
```


