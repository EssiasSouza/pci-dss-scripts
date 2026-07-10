Pelo que conversamos nos últimos dias sobre o PCI DSS, eu focaria em **informações que realmente evidenciem a postura de segurança do workload**, e ignoraria tudo o que é operacional ou informativo.

Eu dividiria em categorias.

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

Aqui você consegue verificar:

* Há mais de um container?
* Existe banco de dados junto?
* Existe sidecar?
* Qual imagem está sendo executada?

---

## 3. Security Context (Muito importante)

Essa é provavelmente a parte mais importante.

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

Esses itens geram diversos controles de auditoria.

Exemplo:

| Verificação              | Esperado       |
| ------------------------ | -------------- |
| runAsNonRoot             | true           |
| privileged               | false          |
| allowPrivilegeEscalation | false          |
| readOnlyRootFilesystem   | true           |
| capabilities.add         | vazio          |
| capabilities.drop        | ALL ou NET_RAW |
| seccompProfile           | RuntimeDefault |

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

Você pode verificar:

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

Esses indicam se o container consome Secrets.

Também vale verificar:

```text
env.value
```

para descobrir se existe senha hardcoded.

---

## 7. ConfigMaps

```text
envFrom.configMapRef
env.valueFrom.configMapKeyRef
```

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

`hostPath` merece atenção especial.

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

Não é um requisito PCI, mas demonstra maturidade operacional.

---

## 11. Networking

```text
hostNetwork
hostPID
hostIPC
dnsPolicy
```

Se algum deles estiver habilitado, merece atenção.

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

Eu só analisaria estas:

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

Essas são úteis para operação, mas pouco agregam à auditoria.

---

# O que eu ignoraria completamente

Esses campos só aumentam o volume do relatório:

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

# Se eu fosse montar um scanner PCI DSS para GKE

Eu criaria uma estrutura semelhante a esta:

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

## Minha sugestão

Como você está desenvolvendo um scanner para a auditoria PCI DSS, eu estruturaria as regras em três níveis:

* **Critical**: `privileged=true`, `allowPrivilegeEscalation=true`, uso de `hostPath`, credenciais em texto claro, aplicação e banco no mesmo Pod.
* **Warning**: ausência de `readOnlyRootFilesystem`, ausência de `runAsNonRoot`, imagens sem digest, uso da tag `latest`.
* **Info**: versão da imagem, recursos (`requests`/`limits`), Helm, Workload Identity, probes, labels e annotations relevantes.

Esse formato produz um relatório objetivo, priorizando os riscos que realmente merecem atenção durante a auditoria.
