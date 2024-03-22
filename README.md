# Point - Lambda Report

## Visão Geral

Este projeto implementa uma solução para geração de relatórios de ponto de funcionários. Ele utiliza uma arquitetura baseada em funções serverless na AWS, onde uma função Lambda é acionada por mensagens em uma fila SQS contendo as informações necessárias para gerar o relatório.

## Componentes

- AWS Lambda: Função serverless que processa as mensagens da fila e gera os relatórios.
- AWS SQS: Fila de mensagens que aciona a função Lambda.
- AWS Secrets Manager: Armazena credenciais seguras utilizadas pela função Lambda.
- AWS S3: Bucket onde os relatórios gerados são armazenados.
- Banco de Dados PostgreSQL: Armazena os registros de ponto dos funcionários.

## Funcionamento

1. Envio da Mensagem: Uma mensagem é enviada para a fila SQS contendo o mês e o ano do relatório desejado, além do token JWT do usuário.
2. Processamento da Mensagem:
A função Lambda decodifica o token JWT para identificar o usuário solicitante.
Extrai o mês e o ano do relatório da mensagem.
Utiliza a classe PointReportUseCase para gerar o relatório do período solicitado.
3. Acesso ao Banco de Dados: A função Lambda utiliza a classe DatabaseHelper para acessar o banco de dados e obter os registros de ponto do funcionário.
4. Geração do Relatório: Com base nos registros de ponto obtidos, a função gera o relatório em formato PDF.
5. Envio por Email: O relatório é enviado por email utilizando a classe MailerAdapter.

## Segurança e Configuração

- JWT (Json Web Token): Utilizado para autenticar o usuário solicitante e obter seu identificador.
- Credenciais de Acesso: As credenciais de acesso ao banco de dados e ao servidor SMTP são armazenadas de forma segura no AWS Secrets Manager e acessadas pela função Lambda durante sua execução.

## Infraestrutura como Código (IaC)

O projeto utiliza Terraform para provisionar e gerenciar a infraestrutura na AWS. Os principais recursos configurados incluem a fila SQS, o bucket S3, as permissões IAM e a função Lambda.

## Pré-requisitos

- Conta na AWS com as permissões necessárias para criar e gerenciar serviços Lambda, IAM, S3, entre outros necessários.
- Repositório no GitHub com o código fonte do projeto.
- Terraform instalado na máquina local (para testes locais).
- Python 3.11 ou superior.

## Configuração Inicial

### AWS Credentials

As credenciais da AWS devem ser configuradas como secrets no GitHub para que o GitHub Actions possa acessá-las. As seguintes secrets devem ser configuradas:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

## Terraform

O Terraform é utilizado para provisionar a infraestrutura necessária na AWS. A configuração específica depende dos recursos que o seu projeto necessita. Certifique-se de que os arquivos de configuração do Terraform (*.tf) estejam no diretório infra/.

## Manutenção

- Atualizações de Código: Para atualizar a função Lambda, basta fazer push das mudanças para a branch main.
- Alterações de Infraestrutura: Para alterar a infraestrutura na AWS, modifique os arquivos do Terraform no diretório infra/ e faça push para a branch main.
- Segurança: Regularmente revise as permissões concedidas tanto nas credenciais da AWS quanto nos serviços provisionados para garantir o mínimo privilégio.
