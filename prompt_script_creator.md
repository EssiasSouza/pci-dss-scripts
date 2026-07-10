Você será meu desenvolvedor que irá projetar e desenvolver minha aplicação para levantamento de evidências para a auditoria de PCI-DSS.
Você é especialista em obtenção de certificação PCI-DSS.

Quero que você crie uma aplicação partindo da estrutura, desenvolvendo cada arquivo apenas quando eu solicitar, pois quero revisar um a um. Siga seguintes instruções para a criação dos scripts.

Vamos focar em **informações que realmente evidenciem a postura de segurança do workload**, e ignorar tudo o que é operacional ou informativo.

Vamos dividir em categorias.

## 1. Identificação do workload (Obrigatório)

Essas informações identificam exatamente o que está sendo auditado.

```text
kind
metadata.name
metadata.namespace
metadata.labels
metadata.annotations.meta.helm.sh/*
spec.replicas
```

Essas permitem responder:

* Qual recurso?
* Em qual namespace?
* Foi criado por Helm?
* Quantas réplicas?

---

## 2. Containers (Obrigatório)

Para cada container:

```text
name
image
imagePullPolicy
ports
command
args
```

Aqui será para verificar:

* Há mais de um container?
* Existe banco de dados junto?
* Existe sidecar?
* Qual imagem está sendo executada?

---

## 3. Security Context (Muito importante)

Essa é a parte mais importante.

```text
securityContext.runAsNonRoot
securityContext.runAsUser
securityContext.runAsGroup
securityContext.allowPrivilegeEscalation
securityContext.privileged
securityContext.readOnlyRootFilesystem
securityContext.capabilities.add
securityContext.capabilities.drop
securityContext.seccompProfile.type
```

Esses itens gerarão diversos controles de auditoria.

Exemplo:

| Regra                           | Severidade | PCI DSS       |
| ------------------------------- | ---------- | ------------- |
| `privileged=true`               | Critical   | 2.2.5         |
| `allowPrivilegeEscalation=true` | Critical   | 2.2.5         |
| `runAsNonRoot=false`            | Warning    | 2.2.5         |
| `readOnlyRootFilesystem=false`  | Warning    | 2.2.5         |
| `hostPath`                      | Critical   | 2.2.5         |
| `latest`                        | Warning    | 6.3.2         |
| Sem digest                      | Warning    | 6.3.2         |
| Secret hardcoded                | Critical   | 3.3.2         |
| Sem requests/limits             | Info       | Boas práticas |
| Sem probes                      | Info       | Boas práticas |
| Workload Identity               | Info       | 8.x           |


---

## 4. Recursos

```text
resources.requests
resources.limits
```

Importante para verificar se o workload possui limites definidos.

---

## 5. Imagem

```text
image
imagePullPolicy
```

Assim poderemos verificar:

* latest?
* digest?
* registry privado?
* registry público?

---

## 6. Secrets

Muito importante.

```text
envFrom.secretRef
env.valueFrom.secretKeyRef
volumes.secret
```

Esses indicarão se o container consome Secrets.

Também vale verificar:

```text
env.value
```

para descobrir se existe senha hardcoded.

Se o nome da variável contém algo como

PASSWORD
SECRET
TOKEN
KEY
ACCESS_KEY
PRIVATE
CERT
CLIENT_SECRET
API_KEY

e utiliza value, então você a aplicação deverá marcar um WARNING.

---

## 7. ConfigMaps

```text
envFrom.configMapRef
env.valueFrom.configMapKeyRef
```

A aplicação não precisa abrir o ConfigMap. Precisa apenas registrar:

Configuration source:
checkout-config

---

## 8. Volumes

```text
volumes
volumeMounts
```

Especialmente:

* hostPath
* secret
* projected
* emptyDir
* persistentVolumeClaim

`hostPath` merecerá atenção especial.

---

## 9. Service Account

```text
serviceAccount
serviceAccountName
automountServiceAccountToken
```

---

## 10. Probes

```text
livenessProbe
readinessProbe
startupProbe
```

Não é um requisito PCI, mas vai demonstrar maturidade operacional.

---

## 11. Networking

```text
hostNetwork
hostPID
hostIPC
dnsPolicy
```

Se algum deles estiver habilitado, merecerá atenção.

---

## 12. Scheduling

```text
nodeSelector
tolerations
affinity
```

Normalmente apenas informativo.

---

## 13. Annotations

Só vamos analisar estas:

```text
iam.gke.io/*
vault.hashicorp.com/*
sidecar.istio.io/*
linkerd.io/*
container.apparmor.*
seccomp.*
```

Ignoraria completamente:

```text
deployment.kubernetes.io/*
autopilot.gke.io/*
kubectl.kubernetes.io/*
meta.helm.sh/*
```

Essas são úteis para operação, mas pouco agregarão à auditoria.

---

# Vamos ignoraria completamente

Esses campos só aumentariam o volume do relatório:

```text
status
managedFields
creationTimestamp
resourceVersion
uid
generation
selfLink
```

Também ignoraria:

```text
terminationMessagePath
terminationMessagePolicy
dnsConfig
restartPolicy
schedulerName
```

Eles dificilmente trazem evidências relevantes para PCI.

---

# Vamos montar um scanner PCI DSS para GKE

Vamos criar essa estrutura:

| Categoria        | Regras                                 |
| ---------------- | -------------------------------------- |
| Identification   | Nome, Namespace, Tipo                  |
| Containers       | Imagens, quantidade, banco + aplicação |
| Security Context | 7 ou 8 verificações                    |
| Resources        | Requests/Limits                        |
| Secrets          | SecretRef, env, hardcoded              |
| Volumes          | hostPath, Secret, PVC                  |
| Service Account  | Token, Workload Identity               |
| Network          | HostNetwork, HostPID                   |
| Image Security   | latest, digest, registry               |
| Probes           | Health Checks                          |

Isso já cobre cerca de **90% das verificações** que podem ser feitas apenas analisando o manifesto do Deployment.

## Atenção

Para este scanner para a auditoria PCI DSS, vamos estrutura as regras em três níveis:

* **Critical**: `privileged=true`, `allowPrivilegeEscalation=true`, uso de `hostPath`, credenciais em texto claro, aplicação e banco no mesmo Pod.
* **Warning**: ausência de `readOnlyRootFilesystem`, ausência de `runAsNonRoot`, imagens sem digest, uso da tag `latest`.
* **Info**: versão da imagem, recursos (`requests`/`limits`), Helm, Workload Identity, probes, labels e annotations relevantes.

Esse formato produz um relatório objetivo, priorizando os riscos que realmente merecem atenção durante a auditoria.

Vamos desenvolver a aplicação em Python.

Essa deverá ser a estrutura.

main.py
│
├── collector.py
│      coleta YAML
│
├── parser.py
│      extrai apenas os campos relevantes
│
├── rules.py
│      executa as regras PCI
│
├── report.py
│      gera Markdown
│
├── logger.py
│      grava logs
│
└── models.py
       estruturas de dados

A aplicação deverá imprimir em "logs/PCI-DSS_evidences_YYYYMMDD_HHMMSS.log" as informações de cada operação.

O resultado do relatório na estrutura de categoria e regras deve ser salvo no arquivo "outputs/relatório.md"

O objetivo final dessa aplicação será fornecer dados suficientes para a avaliação do auditor sobre meu ambiente.

Para não perdermos o contexto, quero que você inicie criando um arquivo de implementation plan. Este será o primeiro arquivo do projeto a ser criado e que irá reger nosso desenvolvimento.

Regras mandatórias:
- Não sugira nenhuma melhoria.
- Não crie nada fora do que está sendo pedido aqui.
- Sempre que for pedido um novo script, cheque os passos do implementation plan se está de acordo com o que foi planejado.
- Sempre cheque o script para validar se existe alguma falha de escrita antes de me entregar.
