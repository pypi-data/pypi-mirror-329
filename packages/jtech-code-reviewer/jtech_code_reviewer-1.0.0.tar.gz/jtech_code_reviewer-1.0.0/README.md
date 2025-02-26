# JTech Code Review Local

Sistema de revisão de código local que utiliza IA para fornecer sugestões de melhorias durante o processo de commit.

## Requisitos

- Python 3.12 ou superior
- Git
- Chave de API do Google (para Vertex AI)

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd jtech-code-review
```

2. Execute o script de instalação:
```bash
chmod +x install.sh
./install.sh
```

3. Configure sua chave API do Google no arquivo `.env`:
```bash
GOOGLE_API_KEY=sua_chave_aqui
```

## Uso

1. Inicie o serviço:
```bash
./start_review_service.sh
```

2. Faça suas alterações no código normalmente

3. Ao tentar fazer um commit, o hook do git irá automaticamente:
   - Analisar as mudanças
   - Mostrar sugestões de melhorias
   - Perguntar se deseja prosseguir com o commit

4. Para parar o serviço:
```bash
./stop_review_service.sh
```

## Funcionalidades

- Análise automática de código durante commits
- Sugestões de melhorias usando IA
- Suporte a diversos tipos de arquivos
- Integração com git hooks

## Opções Avançadas

### Ignorar revisão temporariamente

Para fazer um commit sem revisão de código:
```bash
git commit --no-verify -m "sua mensagem"
```

### Logs do serviço

Os logs do serviço podem ser encontrados em:
```
logs/review_service.log
```

### Configurações personalizadas

Edite o arquivo `.env` para personalizar:
- `PORT`: Porta do servidor local (padrão: 3000)
- `HOST`: Host do servidor (padrão: 127.0.0.1)

## Solução de Problemas

### Serviço não inicia

1. Verifique se a chave API está configurada corretamente
2. Confirme que a porta 3000 está disponível
3. Verifique os logs em `logs/review_service.log`

### Hook não executa

1. Verifique se o serviço está rodando (`curl localhost:3000/health`)
2. Confirme que o arquivo `.git/hooks/pre-commit` tem permissão de execução
3. Verifique se o git está configurado corretamente

## Limitações Atuais

- Atualmente otimizado para revisão de código Java
- Requer conexão com internet para acesso à API do Google
- Uma revisão por vez por arquivo

## Contribuindo

1. Fork o repositório
2. Crie sua feature branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -am 'Adicionando nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.