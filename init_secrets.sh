#!/usr/bin/env bash
set -e

SECRETS_DIR="./secrets"

echo "Inicializando secrets..."

# Cria diretório de secrets caso não exista
mkdir -p "$SECRETS_DIR"

# Função para criar secret seguro sem sobrescrever
create_secret() {
    local filename="$SECRETS_DIR/$1"
    local value="$2"

    if [ -f "$filename" ]; then
        echo "✔ Secret $1 já existe — não sobrescrevendo."
    else
        echo -n "$value" > "$filename"
        echo "✔ Secret $1 criado."
    fi
}

# Função para criar secret aleatório (tokens, senhas)
random_secret() {
    tr -dc 'A-Za-z0-9!@#$%^&*()_+=-' </dev/urandom | head -c 32
}

echo "➡ Criando secrets do InfluxDB..."
create_secret "influxdb_admin_username" "admin"
create_secret "influxdb_admin_password" "$(random_secret)"
create_secret "influxdb_admin_token" "$(random_secret)"

echo "➡ Criando secrets do Grafana..."
create_secret "grafana_admin_username" "admin"
create_secret "grafana_admin_password" "$(random_secret)"

echo "➡ Ajustando permissões..."
chmod 644 "$SECRETS_DIR"/*

echo "🎉 Secrets criados com sucesso!"
echo ""
echo "Arquivos gerados em $SECRETS_DIR:"
ls -l "$SECRETS_DIR"
echo ""
echo "Se quiser visualizar algum secret, use:"
echo "  cat secrets/<nome_do_secret>"
