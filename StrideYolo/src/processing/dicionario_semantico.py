# dicionario_semantico.py

DICIONARIO_COMPONENTES = {
    "rds": "Database",
    "mysql": "Database",
    "mariadb": "Database",
    "elasticache": "Cache",
    "redis": "Cache",
    "api gateway": "API Gateway",
    "gateway": "API Gateway",
    "load balancer": "Load Balancer",
    "auth": "Authentication",
    "authentication": "Authentication",
    "iam": "Authentication",
    "cognito": "Authentication",
    "s3": "Storage",
    "blob storage": "Storage",
    "bucket": "Storage",
    "amplifystoragebucket": "Storage",
    "webuibucket": "Storage",
    "discoverybucket": "Storage",
    "object storage": "Storage",
    "elasticsearch": "Index/Search",
    "opensearch": "Index/Search",
    "couchdb": "Database",
    "sql database": "Database",
    "neptune": "Database",
    "athena": "Database",
    "dynamodb": "Database",
    "curbucket": "Storage",
    "athenaresultsbucket": "Storage",
    "app service": "Frontend Service",
    "cloudfront": "Frontend Service",
    "amplify": "Frontend Service",
    "web ui": "Frontend Service",
    "appconfig": "Configuration",
    "settings": "Configuration",
    "push notifications": "Messaging",
    "pub/sub": "Messaging",
    "messaging": "Messaging",
    "cloud function": "Backend Service",
    "lambda": "Backend Service",
    "aws lambda": "Backend Service",
    "function": "Backend Service",
    "gremlin resolver": "Backend Service",
    "search resolver": "Backend Service",
    "config": "Configuration",
    "codebuild": "DevOps",
    "ec2": "Backend Service",
    "ecs": "Container Service",
    "fargate": "Container Service",
    "container service": "Container Service",
    "container registry": "Container Service",
    "ecr": "Container Service",
    "azure function": "Backend Service",
    "autonomous db": "Database",
    "vpc": "Network",
    "private subnet": "Network",
    "networking": "Network",
    "sdk": "Client SDK",
    "users": "User",
}

def mapear_componente(texto_detectado):
    texto_normalizado = texto_detectado.strip().lower()
    for chave, componente in DICIONARIO_COMPONENTES.items():
        if chave in texto_normalizado:
            return componente
    return "Unknown"

if __name__ == "__main__":
    exemplos = ["Amazon RDS", "AWS Lambda", "Web UI", "Cognito", "Amazon DynamoDB"]
    for exemplo in exemplos:
        print(f"{exemplo} → {mapear_componente(exemplo)}")
