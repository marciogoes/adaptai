# Gerar atividades usando a API do backend
import requests

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("🚀 GERADOR DE ATIVIDADES - AdaptAI")
print("=" * 60)

# 1. Login
print("\n1️⃣ Fazendo login...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "admin@adaptai.com", "password": "admin123"}
)

if login_response.status_code != 200:
    print(f"❌ Erro no login: {login_response.text}")
    exit(1)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("✅ Login OK!")

# 2. Gerar calendário
print("\n2️⃣ Gerando calendário de atividades para PEI 3...")
print("⏳ Isso pode demorar alguns minutos (gerando conteúdo com IA)...")

try:
    response = requests.post(
        f"{BASE_URL}/calendario/gerar",
        headers=headers,
        json={"pei_id": 3},
        timeout=600  # 10 minutos de timeout
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ SUCESSO!")
        print(f"📊 Resumo:")
        print(f"   - Aluno: {data.get('student_name', 'N/A')}")
        print(f"   - Total de objetivos: {data.get('total_objetivos', 0)}")
        print(f"   - Atividades geradas: {data.get('atividades_geradas', 0)}")
        print(f"   - Materiais criados: {data.get('materiais_gerados', 0)}")
        print(f"   - Provas criadas: {data.get('provas_geradas', 0)}")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("❌ Timeout - A operação demorou mais de 10 minutos")
except Exception as e:
    print(f"❌ Erro: {e}")
