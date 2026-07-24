# Relatório Comparativo de Conformidade PCI-DSS 4.0.1
## Gringo Servers - Auditoria 2026

**Data de Referência:** 13 de Julho de 2026
**Documento de Origem do Auditor:** `Orientação_auditor_BR_PCI-DSS Controls 2026_Gringo_Servers_v2.xlsx`
**Documento de Origem do GCP SCC:** `Relatório_GCP-pci-dss-4-0_compliance_2026-07-13.csv`

---

## 1. Resumo Executivo

Este relatório apresenta a comparação entre a grade de controles enviada pelo auditor para a certificação do ambiente **Gringo Servers** e os resultados obtidos a partir do scanner automatizado do **Google Cloud Security Command Center (SCC)**.

### Indicadores Gerais (Escopo do Auditor)
- **Total de Requisitos Mapeados pelo Auditor:** 25
- **Requisitos em Conformidade (GCP SCC):** 1 (4.0%)
- **Requisitos Não-Conformes (GCP SCC):** 12 (48.0%)
- **Requisitos Não Avaliados pelo GCP SCC (Manual/OS-level):** 12 (48.0%)
- **Total de Vulnerabilidades/Desvios (Findings) no GCP:** 639

### Distribuição dos Status
| Status | Quantidade | Percentual | Descrição |
|---|---|---|---|
| **Compliant** | 1 | 4.0% | O GCP SCC validou e não encontrou falhas de conformidade. |
| **Non-compliant** | 12 | 48.0% | O GCP SCC detectou violações ativas que precisam de correção. |
| **Not Assessed** | 12 | 48.0% | Controles que exigem auditoria manual ou configurações internas do S.O. |

---

## 2. Visão Geral dos Controles Mapeados

Abaixo está a tabela consolidada com a situação de cada requisito solicitado pelo auditor:

| Requisito | Tópico (Auditor) | Status GCP SCC | Falhas (Regras GCP) | Total Findings | Observação/Comentário Auditor |
|---|---|---|---|---|---|
| **2.2.1** | Padrões de configuração (Hardening) | ✅ Compliant | 0/8 | 0 | Como a Gringo utiliza GCP, será necessário verificar os padrões aplicáveis e criar se não existirem. |
| **2.2.3** | Isolamento de funções | ⚠️ Not Assessed | 0/0 | 0 | ? |
| **6.3.3** | Gerenciamento de patches | ⚠️ Not Assessed | 0/0 | 0 | Patches no kubernetes? |
| **6.5.3** | Separação entre DEV/HML e Produção | ⚠️ Not Assessed | 0/0 | 0 | Verificar segregação. |
| **10.2.1** | Logs habilitados | ❌ Non-compliant | 12/20 | 140 | Checar |
| **10.2.1.2** | Ações administrativas | ❌ Non-compliant | 12/20 | 140 | Checar |
| **10.2.1.3** | Acesso aos logs | ❌ Non-compliant | 9/10 | 43 | Checar |
| **10.2.1.4** | Tentativas de acesso inválidas | ❌ Non-compliant | 9/10 | 43 | ? |
| **10.2.1.5** | Alterações em contas | ❌ Non-compliant | 12/20 | 140 | (OKTA) |
| **10.2.1.6** | Inicialização dos logs | ❌ Non-compliant | 9/10 | 43 | Checar |
| **10.2.1.7** | Objetos do sistema | ❌ Non-compliant | 9/10 | 43 | ? |
| **10.2.2** | Conteúdo mínimo dos logs | ❌ Non-compliant | 9/10 | 43 | Checar |
| **10.3.1** | Permissão de leitura dos logs | ⚠️ Not Assessed | 0/0 | 0 | Checar |
| **10.3.2** |  | ⚠️ Not Assessed | 0/0 | 0 | - |
| **10.3.3** |  | ⚠️ Not Assessed | 0/0 | 0 | - |
| **10.3.4** |  | ⚠️ Not Assessed | 0/0 | 0 | - |
| **10.4.1** |  | ❌ Non-compliant | 1/2 | 1 | - |
| **10.4.1.1** |  | ❌ Non-compliant | 1/2 | 1 | - |
| **10.4.2** |  | ❌ Non-compliant | 1/2 | 1 | - |
| **10.4.2.1** |  | ⚠️ Not Assessed | 0/0 | 0 | - |
| **10.4.3** |  | ❌ Non-compliant | 1/2 | 1 | - |
| **10.5.1** |  | ⚠️ Not Assessed | 0/0 | 0 | - |
| **10.6.1** |  | ⚠️ Not Assessed | 0/0 | 0 | - |
| **10.6.2** |  | ⚠️ Not Assessed | 0/0 | 0 | - |
| **10.6.3** |  | ⚠️ Not Assessed | 0/0 | 0 | - |

---

## 3. Detalhamento dos Requisitos Não-Conformes (Non-compliant)

Esta seção detalha as violações de conformidade detectadas pelo Google Cloud Security Command Center para os controles mapeados.

### ❌ Requisito 10.2.1 - Logs habilitados
**Descrição do Controle (Inglês):** *Audit logs are enabled and active for all system components and cardholder data.*

**Instruções do Auditor (O que você precisa fazer):** Garantir que todos os sistemas gerem logs de auditoria.

**Nota Interna (Sheet1):** Checar

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `LOAD_BALANCER_LOGGING_DISABLED` | Enable logging for the load balancer backend service. | **Medium** | 43 | 35 |
| `SQL_LOG_DISCONNECTIONS_DISABLED` | The log_disconnections database flag for a Cloud SQL Postgres instance should be set to on. | **Medium** | 33 | 33 |
| `SQL_LOG_CONNECTIONS_DISABLED` | The log_connections database flag for a Cloud SQL Postgres instance should be set to on. | **Medium** | 33 | 31 |
| `SQL_LOG_STATEMENT` | The log_statement database flag for a Cloud SQL Postgres instance should be set to ddl. | **Low** | 33 | 33 |
| `AUDIT_CONFIG_NOT_MONITORED` | Metric filter and alerts should exist for Audit Configuration Changes | **Low** | 1 | 1 |
| `BUCKET_IAM_NOT_MONITORED` | Log metric filter and alerts should exist for Cloud Storage IAM permission changes | **Low** | 1 | 1 |
| `CUSTOM_ROLE_NOT_MONITORED` | Log metric filter and alerts should exist for Custom Role changes | **Low** | 1 | 1 |
| `FIREWALL_NOT_MONITORED` | Log metric filter and alerts should exist for VPC Network Firewall rule changes | **Low** | 1 | 1 |
| `NETWORK_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network changes | **Low** | 1 | 1 |
| `OWNER_NOT_MONITORED` | Log metric filter and alerts should exist for Project Ownership assignments/changes | **Low** | 1 | 1 |
| `ROUTE_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network route changes | **Low** | 1 | 1 |
| `SQL_INSTANCE_NOT_MONITORED` | Log metric filter and alerts should exist for SQL instance configuration changes | **Low** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Habilitar Logging no Load Balancer:** Ativar logs nos backend services dos Load Balancers (35 instâncias reportadas com falha).
- **Configurar Filtros de Métricas e Alertas:** Criar filtros de logs e alertas no Cloud Monitoring para alterações críticas: IAM no Storage, Custom Roles, VPC Firewall, VPC Networks, Project Ownership, VPC Routes, SQL Instances, e Configurações de Auditoria.

### ❌ Requisito 10.2.1.2 - Ações administrativas
**Descrição do Controle (Inglês):** *Audit logs capture all actions taken by any individual with administrative access, including any interactive use of application or system accounts.*

**Instruções do Auditor (O que você precisa fazer):** Registrar todas as ações executadas por administradores.

**Nota Interna (Sheet1):** Checar

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `LOAD_BALANCER_LOGGING_DISABLED` | Enable logging for the load balancer backend service. | **Medium** | 43 | 35 |
| `SQL_LOG_DISCONNECTIONS_DISABLED` | The log_disconnections database flag for a Cloud SQL Postgres instance should be set to on. | **Medium** | 33 | 33 |
| `SQL_LOG_CONNECTIONS_DISABLED` | The log_connections database flag for a Cloud SQL Postgres instance should be set to on. | **Medium** | 33 | 31 |
| `SQL_LOG_STATEMENT` | The log_statement database flag for a Cloud SQL Postgres instance should be set to ddl. | **Low** | 33 | 33 |
| `AUDIT_CONFIG_NOT_MONITORED` | Metric filter and alerts should exist for Audit Configuration Changes | **Low** | 1 | 1 |
| `BUCKET_IAM_NOT_MONITORED` | Log metric filter and alerts should exist for Cloud Storage IAM permission changes | **Low** | 1 | 1 |
| `CUSTOM_ROLE_NOT_MONITORED` | Log metric filter and alerts should exist for Custom Role changes | **Low** | 1 | 1 |
| `FIREWALL_NOT_MONITORED` | Log metric filter and alerts should exist for VPC Network Firewall rule changes | **Low** | 1 | 1 |
| `NETWORK_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network changes | **Low** | 1 | 1 |
| `OWNER_NOT_MONITORED` | Log metric filter and alerts should exist for Project Ownership assignments/changes | **Low** | 1 | 1 |
| `ROUTE_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network route changes | **Low** | 1 | 1 |
| `SQL_INSTANCE_NOT_MONITORED` | Log metric filter and alerts should exist for SQL instance configuration changes | **Low** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Habilitar Logging no Load Balancer:** Ativar logs nos backend services dos Load Balancers (35 instâncias reportadas com falha).
- **Configurar Filtros de Métricas e Alertas:** Criar filtros de logs e alertas no Cloud Monitoring para alterações críticas: IAM no Storage, Custom Roles, VPC Firewall, VPC Networks, Project Ownership, VPC Routes, SQL Instances, e Configurações de Auditoria.

### ❌ Requisito 10.2.1.3 - Acesso aos logs
**Descrição do Controle (Inglês):** *Audit logs capture all access to audit logs.*

**Instruções do Auditor (O que você precisa fazer):** Registrar quem acessou os arquivos de log.

**Nota Interna (Sheet1):** Checar

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `LOAD_BALANCER_LOGGING_DISABLED` | Enable logging for the load balancer backend service. | **Medium** | 43 | 35 |
| `AUDIT_CONFIG_NOT_MONITORED` | Metric filter and alerts should exist for Audit Configuration Changes | **Low** | 1 | 1 |
| `BUCKET_IAM_NOT_MONITORED` | Log metric filter and alerts should exist for Cloud Storage IAM permission changes | **Low** | 1 | 1 |
| `CUSTOM_ROLE_NOT_MONITORED` | Log metric filter and alerts should exist for Custom Role changes | **Low** | 1 | 1 |
| `FIREWALL_NOT_MONITORED` | Log metric filter and alerts should exist for VPC Network Firewall rule changes | **Low** | 1 | 1 |
| `NETWORK_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network changes | **Low** | 1 | 1 |
| `OWNER_NOT_MONITORED` | Log metric filter and alerts should exist for Project Ownership assignments/changes | **Low** | 1 | 1 |
| `ROUTE_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network route changes | **Low** | 1 | 1 |
| `SQL_INSTANCE_NOT_MONITORED` | Log metric filter and alerts should exist for SQL instance configuration changes | **Low** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Habilitar Logging no Load Balancer:** Ativar logs nos backend services dos Load Balancers (35 instâncias reportadas com falha).
- **Configurar Filtros de Métricas e Alertas:** Criar filtros de logs e alertas no Cloud Monitoring para alterações críticas: IAM no Storage, Custom Roles, VPC Firewall, VPC Networks, Project Ownership, VPC Routes, SQL Instances, e Configurações de Auditoria.

### ❌ Requisito 10.2.1.4 - Tentativas de acesso inválidas
**Descrição do Controle (Inglês):** *Audit logs capture all invalid logical access attempts.*

**Instruções do Auditor (O que você precisa fazer):** Registrar todas as tentativas de login malsucedidas.

**Nota Interna (Sheet1):** ?

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `LOAD_BALANCER_LOGGING_DISABLED` | Enable logging for the load balancer backend service. | **Medium** | 43 | 35 |
| `AUDIT_CONFIG_NOT_MONITORED` | Metric filter and alerts should exist for Audit Configuration Changes | **Low** | 1 | 1 |
| `BUCKET_IAM_NOT_MONITORED` | Log metric filter and alerts should exist for Cloud Storage IAM permission changes | **Low** | 1 | 1 |
| `CUSTOM_ROLE_NOT_MONITORED` | Log metric filter and alerts should exist for Custom Role changes | **Low** | 1 | 1 |
| `FIREWALL_NOT_MONITORED` | Log metric filter and alerts should exist for VPC Network Firewall rule changes | **Low** | 1 | 1 |
| `NETWORK_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network changes | **Low** | 1 | 1 |
| `OWNER_NOT_MONITORED` | Log metric filter and alerts should exist for Project Ownership assignments/changes | **Low** | 1 | 1 |
| `ROUTE_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network route changes | **Low** | 1 | 1 |
| `SQL_INSTANCE_NOT_MONITORED` | Log metric filter and alerts should exist for SQL instance configuration changes | **Low** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Habilitar Logging no Load Balancer:** Ativar logs nos backend services dos Load Balancers (35 instâncias reportadas com falha).
- **Configurar Filtros de Métricas e Alertas:** Criar filtros de logs e alertas no Cloud Monitoring para alterações críticas: IAM no Storage, Custom Roles, VPC Firewall, VPC Networks, Project Ownership, VPC Routes, SQL Instances, e Configurações de Auditoria.

### ❌ Requisito 10.2.1.5 - Alterações em contas
**Descrição do Controle (Inglês):** *Audit logs capture all changes to identification and authentication credentials including, but not limited to:
• Creation of new accounts.
• Elevation of privileges.
• All changes, additions, or deletions to accounts with administrative access.*

**Instruções do Auditor (O que você precisa fazer):** Registrar criação, exclusão, alteração de privilégios e mudanças em contas administrativas.

**Nota Interna (Sheet1):** (OKTA)

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `LOAD_BALANCER_LOGGING_DISABLED` | Enable logging for the load balancer backend service. | **Medium** | 43 | 35 |
| `SQL_LOG_DISCONNECTIONS_DISABLED` | The log_disconnections database flag for a Cloud SQL Postgres instance should be set to on. | **Medium** | 33 | 33 |
| `SQL_LOG_CONNECTIONS_DISABLED` | The log_connections database flag for a Cloud SQL Postgres instance should be set to on. | **Medium** | 33 | 31 |
| `SQL_LOG_STATEMENT` | The log_statement database flag for a Cloud SQL Postgres instance should be set to ddl. | **Low** | 33 | 33 |
| `AUDIT_CONFIG_NOT_MONITORED` | Metric filter and alerts should exist for Audit Configuration Changes | **Low** | 1 | 1 |
| `BUCKET_IAM_NOT_MONITORED` | Log metric filter and alerts should exist for Cloud Storage IAM permission changes | **Low** | 1 | 1 |
| `CUSTOM_ROLE_NOT_MONITORED` | Log metric filter and alerts should exist for Custom Role changes | **Low** | 1 | 1 |
| `FIREWALL_NOT_MONITORED` | Log metric filter and alerts should exist for VPC Network Firewall rule changes | **Low** | 1 | 1 |
| `NETWORK_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network changes | **Low** | 1 | 1 |
| `OWNER_NOT_MONITORED` | Log metric filter and alerts should exist for Project Ownership assignments/changes | **Low** | 1 | 1 |
| `ROUTE_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network route changes | **Low** | 1 | 1 |
| `SQL_INSTANCE_NOT_MONITORED` | Log metric filter and alerts should exist for SQL instance configuration changes | **Low** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Habilitar Logging no Load Balancer:** Ativar logs nos backend services dos Load Balancers (35 instâncias reportadas com falha).
- **Configurar Filtros de Métricas e Alertas:** Criar filtros de logs e alertas no Cloud Monitoring para alterações críticas: IAM no Storage, Custom Roles, VPC Firewall, VPC Networks, Project Ownership, VPC Routes, SQL Instances, e Configurações de Auditoria.

### ❌ Requisito 10.2.1.6 - Inicialização dos logs
**Descrição do Controle (Inglês):** *Audit logs capture the following:
• All initialization of new audit logs, and
• All starting, stopping, or pausing of the existing audit logs.*

**Instruções do Auditor (O que você precisa fazer):** Registrar quando o serviço de logs é iniciado, parado ou pausado.

**Nota Interna (Sheet1):** Checar

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `LOAD_BALANCER_LOGGING_DISABLED` | Enable logging for the load balancer backend service. | **Medium** | 43 | 35 |
| `AUDIT_CONFIG_NOT_MONITORED` | Metric filter and alerts should exist for Audit Configuration Changes | **Low** | 1 | 1 |
| `BUCKET_IAM_NOT_MONITORED` | Log metric filter and alerts should exist for Cloud Storage IAM permission changes | **Low** | 1 | 1 |
| `CUSTOM_ROLE_NOT_MONITORED` | Log metric filter and alerts should exist for Custom Role changes | **Low** | 1 | 1 |
| `FIREWALL_NOT_MONITORED` | Log metric filter and alerts should exist for VPC Network Firewall rule changes | **Low** | 1 | 1 |
| `NETWORK_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network changes | **Low** | 1 | 1 |
| `OWNER_NOT_MONITORED` | Log metric filter and alerts should exist for Project Ownership assignments/changes | **Low** | 1 | 1 |
| `ROUTE_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network route changes | **Low** | 1 | 1 |
| `SQL_INSTANCE_NOT_MONITORED` | Log metric filter and alerts should exist for SQL instance configuration changes | **Low** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Habilitar Logging no Load Balancer:** Ativar logs nos backend services dos Load Balancers (35 instâncias reportadas com falha).
- **Configurar Filtros de Métricas e Alertas:** Criar filtros de logs e alertas no Cloud Monitoring para alterações críticas: IAM no Storage, Custom Roles, VPC Firewall, VPC Networks, Project Ownership, VPC Routes, SQL Instances, e Configurações de Auditoria.

### ❌ Requisito 10.2.1.7 - Objetos do sistema
**Descrição do Controle (Inglês):** *Audit logs capture all creation and deletionof system-level objects.*

**Instruções do Auditor (O que você precisa fazer):** Registrar criação e exclusão de objetos importantes do sistema.

**Nota Interna (Sheet1):** ?

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `LOAD_BALANCER_LOGGING_DISABLED` | Enable logging for the load balancer backend service. | **Medium** | 43 | 35 |
| `AUDIT_CONFIG_NOT_MONITORED` | Metric filter and alerts should exist for Audit Configuration Changes | **Low** | 1 | 1 |
| `BUCKET_IAM_NOT_MONITORED` | Log metric filter and alerts should exist for Cloud Storage IAM permission changes | **Low** | 1 | 1 |
| `CUSTOM_ROLE_NOT_MONITORED` | Log metric filter and alerts should exist for Custom Role changes | **Low** | 1 | 1 |
| `FIREWALL_NOT_MONITORED` | Log metric filter and alerts should exist for VPC Network Firewall rule changes | **Low** | 1 | 1 |
| `NETWORK_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network changes | **Low** | 1 | 1 |
| `OWNER_NOT_MONITORED` | Log metric filter and alerts should exist for Project Ownership assignments/changes | **Low** | 1 | 1 |
| `ROUTE_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network route changes | **Low** | 1 | 1 |
| `SQL_INSTANCE_NOT_MONITORED` | Log metric filter and alerts should exist for SQL instance configuration changes | **Low** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Habilitar Logging no Load Balancer:** Ativar logs nos backend services dos Load Balancers (35 instâncias reportadas com falha).
- **Configurar Filtros de Métricas e Alertas:** Criar filtros de logs e alertas no Cloud Monitoring para alterações críticas: IAM no Storage, Custom Roles, VPC Firewall, VPC Networks, Project Ownership, VPC Routes, SQL Instances, e Configurações de Auditoria.

### ❌ Requisito 10.2.2 - Conteúdo mínimo dos logs
**Descrição do Controle (Inglês):** *Audit logs record the following details for each auditable event:
• User identification.
• Type of event.
• Date and time.
• Success and failure indication.
• Origination of event.
• Identity or name of affected data, system component, resource, or service (for example, name and protocol).*

**Instruções do Auditor (O que você precisa fazer):** Garantir que cada log contenha usuário, data, hora, origem, resultado e recurso afetado.

**Nota Interna (Sheet1):** Checar

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `LOAD_BALANCER_LOGGING_DISABLED` | Enable logging for the load balancer backend service. | **Medium** | 43 | 35 |
| `AUDIT_CONFIG_NOT_MONITORED` | Metric filter and alerts should exist for Audit Configuration Changes | **Low** | 1 | 1 |
| `BUCKET_IAM_NOT_MONITORED` | Log metric filter and alerts should exist for Cloud Storage IAM permission changes | **Low** | 1 | 1 |
| `CUSTOM_ROLE_NOT_MONITORED` | Log metric filter and alerts should exist for Custom Role changes | **Low** | 1 | 1 |
| `FIREWALL_NOT_MONITORED` | Log metric filter and alerts should exist for VPC Network Firewall rule changes | **Low** | 1 | 1 |
| `NETWORK_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network changes | **Low** | 1 | 1 |
| `OWNER_NOT_MONITORED` | Log metric filter and alerts should exist for Project Ownership assignments/changes | **Low** | 1 | 1 |
| `ROUTE_NOT_MONITORED` | Log metric filter and alerts should exist for VPC network route changes | **Low** | 1 | 1 |
| `SQL_INSTANCE_NOT_MONITORED` | Log metric filter and alerts should exist for SQL instance configuration changes | **Low** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Verificar a Estrutura dos Logs de Auditoria:** Garantir que os logs de auditoria do GCP (Admin Activity e Data Access) estejam ativados e integrados para registrar todos os metadados exigidos (usuário, data/hora, tipo de ação, etc.). Habilitar logs nos Load Balancers (35 instâncias pendentes) ajudará a complementar essas informações.

### ❌ Requisito 10.4.1 - 
**Descrição do Controle (Inglês):** *The following audit logs are reviewed at least once daily:
• All security events.
• Logs of all system components that store, process, or transmit CHD and/or SAD.
• Logs of all critical system components.
• Logs of all servers and system components that perform security functions (for example, network security controls, intrusion-detection systems/intrusion-prevention systems (IDS/IPS),
authentication servers).*

**Instruções do Auditor (O que você precisa fazer):** 

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `DNS_LOGGING_DISABLED` | DNS logging should be enabled for VPC networks | **Medium** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Ativar Logging de DNS:** Ativar os logs de consulta (query logging) para as redes VPC no Cloud DNS (1 rede sem log habilitado).

### ❌ Requisito 10.4.1.1 - 
**Descrição do Controle (Inglês):** *Automated mechanisms are used to perform audit log reviews.*

**Instruções do Auditor (O que você precisa fazer):** 

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `DNS_LOGGING_DISABLED` | DNS logging should be enabled for VPC networks | **Medium** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Ativar Logging de DNS:** Ativar os logs de consulta (query logging) para as redes VPC no Cloud DNS (1 rede sem log habilitado).

### ❌ Requisito 10.4.2 - 
**Descrição do Controle (Inglês):** *Logs of all other system components (those not specified in Requirement 10.4.1) are reviewed periodically.*

**Instruções do Auditor (O que você precisa fazer):** 

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `DNS_LOGGING_DISABLED` | DNS logging should be enabled for VPC networks | **Medium** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Ativar Logging de DNS:** Ativar os logs de consulta (query logging) para as redes VPC no Cloud DNS (1 rede sem log habilitado).

### ❌ Requisito 10.4.3 - 
**Descrição do Controle (Inglês):** *Exceptions and anomalies identified during the review process are addressed.*

**Instruções do Auditor (O que você precisa fazer):** 

**Regras Reprovadas no GCP SCC:**
| Categoria da Regra | Regra Avaliada | Severidade | Recursos Afetados | Qtd Findings |
|---|---|---|---|---|
| `DNS_LOGGING_DISABLED` | DNS logging should be enabled for VPC networks | **Medium** | 1 | 1 |

**Plano de Ação Recomendado:**
- **Ativar Logging de DNS:** Ativar os logs de consulta (query logging) para as redes VPC no Cloud DNS (1 rede sem log habilitado).

---

## 4. Requisitos Não Avaliados pelo GCP SCC (Not Assessed)

Os seguintes requisitos não puderam ser verificados de forma automatizada pelo Security Command Center do GCP. Eles necessitam de evidências manuais ou de configurações que residem dentro do sistema operacional (S.O.) ou de políticas corporativas.

### ⚠️ Requisito 2.2.3 - Isolamento de funções
**Descrição do Controle (Inglês):** *Primary functions requiring different security levels are managed as follows:
• Only one primary function exists on a system component,
OR
• Primary functions with differing security levels that exist on the same system component are isolated from each other,
OR
• Primary functions with differing security levels on the same system component are all secured to the level required by the function with the highest security need.*

**Instruções do Auditor (O que você precisa fazer):** Garantir que funções com níveis diferentes de segurança estejam separadas ou protegidas pelo maior nível de segurança.

**Nota do Auditor:** Deve ser gerado um inventário para a Gringo com os componentes e funções primárias (ex: aplicação, banco, serviços). 

**Nota Interna (Sheet1):** ?

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** O GCP valida configurações de nuvem, mas o isolamento de funções (ex: separar banco de dados e aplicação na mesma VM) é um controle lógico interno da VM ou da arquitetura do Kubernetes.
- **Ação Necessária:** Gerar e apresentar um inventário detalhado de componentes com suas funções primárias e demonstrar a segregação de ambientes (ex: via namespaces isolados no GKE ou instâncias dedicadas de VM/Cloud SQL).

### ⚠️ Requisito 6.3.3 - Gerenciamento de patches
**Descrição do Controle (Inglês):** *All system components are protected from known vulnerabilities by installing applicable security patches/updates as follows:
• Patches/updates for critical vulnerabilities (identified according to the risk ranking process at Requirement 6.3.1) are installed within one month of release.
• All other applicable security patches/updates are installed within an appropriate time frame as determined by the entity’s assessment of the criticality of the risk to the environment as identified according to the risk ranking process at Requirement 6.3.1.*

**Instruções do Auditor (O que você precisa fazer):** Aplicar patches críticos em até 30 dias e os demais conforme análise de risco.

**Nota Interna (Sheet1):** Patches no kubernetes?

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** O gerenciamento de patches de segurança de sistemas operacionais e aplicações internas não é monitorado por regras de infraestrutura global da nuvem sem agentes de OS.
- **Ação Necessária:** Demonstrar o processo de aplicação de patches (Kubernetes e VMs), comprovando que patches críticos são aplicados em até 30 dias.

### ⚠️ Requisito 6.5.3 - Separação entre DEV/HML e Produção
**Descrição do Controle (Inglês):** *Pre-production environments are separated from production environments and the separation is enforced with access controls.*

**Instruções do Auditor (O que você precisa fazer):** Impedir que ambientes de pré-produção tenham acesso direto à produção.

**Nota Interna (Sheet1):** Verificar segregação.

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** A separação física ou lógica de ambientes DEV/HML e PRD precisa ser demonstrada através de regras de acesso (IAM) e segmentação de VPCs.
- **Ação Necessária:** Apresentar a documentação de redes e permissões IAM que impedem o acesso cruzado entre ambientes de homologação e produção.

### ⚠️ Requisito 10.3.1 - Permissão de leitura dos logs
**Descrição do Controle (Inglês):** *Read access to audit logs files is limited to those with a job-related need.*

**Instruções do Auditor (O que você precisa fazer):** Apenas pessoas autorizadas podem visualizar os logs.

**Nota Interna (Sheet1):** Checar

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** O controle de acesso a arquivos de log (permissão de leitura e proteção de escrita) geralmente é gerenciado a nível de sistema operacional ou via IAM nas permissões do Cloud Logging.
- **Ação Necessária:** Demonstrar que as permissões de IAM para visualização de logs (ex: roles/logging.viewer) estão restritas a pessoas autorizadas e que os logs exportados (ex: buckets de Cloud Storage ou BigQuery) possuem controle de acesso estrito.

### ⚠️ Requisito 10.3.2 - 
**Descrição do Controle (Inglês):** *Audit log files are protected to prevent modifications by individuals.*

**Instruções do Auditor (O que você precisa fazer):** 

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** O controle de acesso a arquivos de log (permissão de leitura e proteção de escrita) geralmente é gerenciado a nível de sistema operacional ou via IAM nas permissões do Cloud Logging.
- **Ação Necessária:** Demonstrar que as permissões de IAM para visualização de logs (ex: roles/logging.viewer) estão restritas a pessoas autorizadas e que os logs exportados (ex: buckets de Cloud Storage ou BigQuery) possuem controle de acesso estrito.

### ⚠️ Requisito 10.3.3 - 
**Descrição do Controle (Inglês):** *Audit log files, including those for external facing technologies, are promptly backed up to a secure, central, internal log server(s) or other media that is difficult to modify.*

**Instruções do Auditor (O que você precisa fazer):** 

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** O controle de acesso a arquivos de log (permissão de leitura e proteção de escrita) geralmente é gerenciado a nível de sistema operacional ou via IAM nas permissões do Cloud Logging.
- **Ação Necessária:** Demonstrar que as permissões de IAM para visualização de logs (ex: roles/logging.viewer) estão restritas a pessoas autorizadas e que os logs exportados (ex: buckets de Cloud Storage ou BigQuery) possuem controle de acesso estrito.

### ⚠️ Requisito 10.3.4 - 
**Descrição do Controle (Inglês):** *File integrity monitoring or change-detection mechanisms is used on audit logs to ensure that existing log data cannot be changed without generating alerts.*

**Instruções do Auditor (O que você precisa fazer):** 

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** O controle de acesso a arquivos de log (permissão de leitura e proteção de escrita) geralmente é gerenciado a nível de sistema operacional ou via IAM nas permissões do Cloud Logging.
- **Ação Necessária:** Demonstrar que as permissões de IAM para visualização de logs (ex: roles/logging.viewer) estão restritas a pessoas autorizadas e que os logs exportados (ex: buckets de Cloud Storage ou BigQuery) possuem controle de acesso estrito.

### ⚠️ Requisito 10.4.2.1 - 
**Descrição do Controle (Inglês):** *The frequency of periodic log reviews for all other system components (not defined in Requirement 10.4.1) is defined in the entity’s targeted risk analysis, which is performed according to all elements specified in Requirement 12.3.1*

**Instruções do Auditor (O que você precisa fazer):** 

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** A revisão de logs e identificação de anomalias depende de ferramentas de SIEM ou de processos diários de monitoramento operacional.
- **Ação Necessária:** Apresentar a política de revisão de logs e como os alertas críticos são encaminhados para a equipe responsável.

### ⚠️ Requisito 10.5.1 - 
**Descrição do Controle (Inglês):** *Retain audit log history for at least 12 months, with at least the most recent three months immediately available for analysis.*

**Instruções do Auditor (O que você precisa fazer):** 

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** O tempo de retenção de logs é uma configuração do bucket de logs do Cloud Logging (geralmente padrão de 30 dias, mas PCI exige retenção de 1 ano, sendo 3 meses imediatamente disponíveis).
- **Ação Necessária:** Configurar a retenção dos buckets de log do Cloud Logging ou exportar os logs para Cloud Storage com política de retenção de 365 dias, apresentando essa evidência ao auditor.

### ⚠️ Requisito 10.6.1 - 
**Descrição do Controle (Inglês):** *System clocks and time are synchronized using time-synchronization technology.*

**Instruções do Auditor (O que você precisa fazer):** 

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** Configuração de sincronização de hora (NTP) é um ajuste a nível de sistema operacional (embora a infraestrutura do GCP sincronize as instâncias automaticamente).
- **Ação Necessária:** Fornecer as configurações de NTP (`ntpd` ou `systemd-timesyncd`) das VMs e do GKE que demonstrem a sincronização ativa com servidores confiáveis (como metadata.google.internal).

### ⚠️ Requisito 10.6.2 - 
**Descrição do Controle (Inglês):** *Systems are configured to the correct and consistent time as follows:
• One or more designated time servers are in use.
• Only the designated central time server(s) receives time from external sources.
• Time received from external sources is based on International Atomic Time or Coordinated Universal Time (UTC).
• The designated time server(s) accept time updates only from specific industry-accepted external sources.
• Where there is more than one designated time server, the time servers peer with one another to keep accurate time.
• Internal systems receive time information only from designated central time server(s).*

**Instruções do Auditor (O que você precisa fazer):** 

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** Configuração de sincronização de hora (NTP) é um ajuste a nível de sistema operacional (embora a infraestrutura do GCP sincronize as instâncias automaticamente).
- **Ação Necessária:** Fornecer as configurações de NTP (`ntpd` ou `systemd-timesyncd`) das VMs e do GKE que demonstrem a sincronização ativa com servidores confiáveis (como metadata.google.internal).

### ⚠️ Requisito 10.6.3 - 
**Descrição do Controle (Inglês):** *Time synchronization settings and data are protected as follows:
• Access to time data is restricted to only personnel with a business need.
• Any changes to time settings on critical systems are logged, monitored, and reviewed.*

**Instruções do Auditor (O que você precisa fazer):** 

**Justificativa de Ausência no GCP SCC e Próximos Passos:**
- **Motivo:** Configuração de sincronização de hora (NTP) é um ajuste a nível de sistema operacional (embora a infraestrutura do GCP sincronize as instâncias automaticamente).
- **Ação Necessária:** Fornecer as configurações de NTP (`ntpd` ou `systemd-timesyncd`) das VMs e do GKE que demonstrem a sincronização ativa com servidores confiáveis (como metadata.google.internal).