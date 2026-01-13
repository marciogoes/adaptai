"""
🏫 SCRIPT DE CONFIGURAÇÃO INICIAL - AdaptAI
Configura escolas, professores, alunos e super admin

Executar com: python -m app.scripts.setup_inicial
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.escola import Escola, ConfiguracaoEscola
from app.core.security import get_password_hash
from datetime import datetime, date


def criar_super_admin(db: Session) -> User:
    """Cria o Super Admin do sistema"""
    print("\n🔐 Verificando Super Admin...")
    
    admin = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
    
    if admin:
        print(f"   ✅ Super Admin já existe: {admin.email}")
        return admin
    
    admin = User(
        name="Administrador AdaptAI",
        email="admin@adaptai.com.br",
        hashed_password=get_password_hash("Admin@2024"),
        role=UserRole.SUPER_ADMIN,
        is_active=True,
        escola_id=None  # Super admin não pertence a nenhuma escola específica
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"   ✅ Super Admin criado: {admin.email}")
    print(f"   📧 Email: admin@adaptai.com.br")
    print(f"   🔑 Senha: Admin@2024")
    
    return admin


def criar_escola(db: Session) -> Escola:
    """Cria uma escola de demonstração"""
    print("\n🏫 Verificando Escola...")
    
    escola = db.query(Escola).filter(Escola.email == "contato@escolainclusiva.com.br").first()
    
    if escola:
        print(f"   ✅ Escola já existe: {escola.nome}")
        return escola
    
    escola = Escola(
        nome="Escola Inclusiva Modelo",
        nome_fantasia="Escola Inclusiva",
        email="contato@escolainclusiva.com.br",
        telefone="(11) 3456-7890",
        tipo="ESCOLA",
        segmento="Educação Especial",
        cidade="São Paulo",
        estado="SP",
        ativa=True,
        cor_primaria="#8B5CF6",
        cor_secundaria="#EC4899"
    )
    
    db.add(escola)
    db.commit()
    db.refresh(escola)
    
    # Criar configuração da escola
    config = ConfiguracaoEscola(
        escola_id=escola.id,
        modelo_ia_preferido="claude-3-5-sonnet-20241022",
        quantidade_questoes_padrao=5,
        dificuldade_padrao="medio",
        notificacoes_email=True,
        pei_automatico_ativo=True,
        materiais_adaptativos_ativo=True,
        lgpd_ativo=True
    )
    db.add(config)
    db.commit()
    
    print(f"   ✅ Escola criada: {escola.nome}")
    
    return escola


def criar_professores(db: Session, escola: Escola) -> dict:
    """Cria os professores no sistema"""
    print("\n👨‍🏫 Configurando Professores...")
    
    professores = {}
    
    # Professor 1: Márcio Góes do Nascimento
    prof1_email = "marcio.goes@adaptai.com.br"
    prof1 = db.query(User).filter(User.email == prof1_email).first()
    
    if not prof1:
        prof1 = User(
            name="Márcio Góes do Nascimento",
            email=prof1_email,
            hashed_password=get_password_hash("Prof@2024"),
            role=UserRole.TEACHER,
            is_active=True,
            escola_id=escola.id
        )
        db.add(prof1)
        db.commit()
        db.refresh(prof1)
        print(f"   ✅ Professor criado: {prof1.name}")
        print(f"      📧 Email: {prof1_email}")
        print(f"      🔑 Senha: Prof@2024")
    else:
        # Atualizar escola se não tiver
        if not prof1.escola_id:
            prof1.escola_id = escola.id
            db.commit()
        print(f"   ✅ Professor já existe: {prof1.name}")
    
    professores["marcio"] = prof1
    
    # Professor 2: Fábio Roberto Albuquerque Azevedo
    prof2_email = "fabio.azevedo@adaptai.com.br"
    prof2 = db.query(User).filter(User.email == prof2_email).first()
    
    if not prof2:
        prof2 = User(
            name="Fábio Roberto Albuquerque Azevedo",
            email=prof2_email,
            hashed_password=get_password_hash("Prof@2024"),
            role=UserRole.TEACHER,
            is_active=True,
            escola_id=escola.id
        )
        db.add(prof2)
        db.commit()
        db.refresh(prof2)
        print(f"   ✅ Professor criado: {prof2.name}")
        print(f"      📧 Email: {prof2_email}")
        print(f"      🔑 Senha: Prof@2024")
    else:
        if not prof2.escola_id:
            prof2.escola_id = escola.id
            db.commit()
        print(f"   ✅ Professor já existe: {prof2.name}")
    
    professores["fabio"] = prof2
    
    # Professor Ad-Hoc (sem escola) para demonstração
    prof3_email = "professor.adhoc@adaptai.com.br"
    prof3 = db.query(User).filter(User.email == prof3_email).first()
    
    if not prof3:
        prof3 = User(
            name="Professor Independente",
            email=prof3_email,
            hashed_password=get_password_hash("Prof@2024"),
            role=UserRole.TEACHER,
            is_active=True,
            escola_id=None  # Sem escola - professor ad-hoc
        )
        db.add(prof3)
        db.commit()
        db.refresh(prof3)
        print(f"   ✅ Professor Ad-Hoc criado: {prof3.name}")
        print(f"      📧 Email: {prof3_email}")
        print(f"      🔑 Senha: Prof@2024")
        print(f"      ⚠️  SEM ESCOLA (Ad-Hoc)")
    else:
        print(f"   ✅ Professor Ad-Hoc já existe: {prof3.name}")
    
    professores["adhoc"] = prof3
    
    return professores


def associar_alunos(db: Session, professores: dict, escola: Escola):
    """Associa os alunos aos professores corretos"""
    print("\n👨‍🎓 Associando Alunos aos Professores...")
    
    # Mapeamento de alunos para professores
    mapeamento = {
        "MARCIO GOES DO NASCIMENTO JUNIOR": "marcio",
        "MÁRCIO GOES DO NASCIMENTO JUNIOR": "marcio",
        "CASSIO ANTONIO FERREIRA BASTOS GOES DO NASCIMENTO": "marcio",
        "CÁSSIO ANTONIO FERREIRA BASTOS GOES DO NASCIMENTO": "marcio",
        "ENRICO MELO MOTA AZEVEDO": "fabio",
    }
    
    # Buscar todos os alunos
    alunos = db.query(Student).all()
    
    for aluno in alunos:
        nome_upper = aluno.name.upper()
        
        # Verificar se está no mapeamento
        professor_key = None
        for nome_map, key in mapeamento.items():
            if nome_map in nome_upper or nome_upper in nome_map:
                professor_key = key
                break
        
        if professor_key and professor_key in professores:
            professor = professores[professor_key]
            
            if aluno.created_by_user_id != professor.id:
                aluno.created_by_user_id = professor.id
                aluno.escola_id = escola.id
                db.commit()
                print(f"   ✅ {aluno.name} → Professor {professor.name}")
            else:
                print(f"   ➡️  {aluno.name} já está com Professor {professor.name}")
        else:
            print(f"   ⚠️  {aluno.name} - sem mapeamento definido")
    
    # Criar alunos de demonstração se não existirem
    criar_alunos_demo(db, professores, escola)


def criar_alunos_demo(db: Session, professores: dict, escola: Escola):
    """Cria alunos de demonstração se não existirem"""
    print("\n📚 Verificando Alunos de Demonstração...")
    
    alunos_demo = [
        {
            "name": "MARCIO GOES DO NASCIMENTO JUNIOR",
            "email": "marcio.junior@aluno.adaptai.com.br",
            "grade_level": "5º ano",
            "birth_date": date(2014, 5, 15),
            "diagnosis": {"tea": {"level": 1}, "tdah": False},
            "professor": "marcio"
        },
        {
            "name": "CASSIO ANTONIO FERREIRA BASTOS GOES DO NASCIMENTO",
            "email": "cassio.goes@aluno.adaptai.com.br",
            "grade_level": "3º ano",
            "birth_date": date(2016, 8, 22),
            "diagnosis": {"tea": False, "tdah": True},
            "professor": "marcio"
        },
        {
            "name": "ENRICO MELO MOTA AZEVEDO",
            "email": "enrico.azevedo@aluno.adaptai.com.br",
            "grade_level": "4º ano",
            "birth_date": date(2015, 3, 10),
            "diagnosis": {"tea": {"level": 2}, "tdah": False},
            "professor": "fabio"
        },
    ]
    
    for aluno_data in alunos_demo:
        aluno = db.query(Student).filter(
            Student.name.ilike(f"%{aluno_data['name']}%")
        ).first()
        
        if not aluno:
            professor = professores.get(aluno_data["professor"])
            if professor:
                aluno = Student(
                    name=aluno_data["name"],
                    email=aluno_data["email"],
                    hashed_password=get_password_hash("Aluno@2024"),
                    grade_level=aluno_data["grade_level"],
                    birth_date=aluno_data["birth_date"],
                    diagnosis=aluno_data["diagnosis"],
                    is_active=True,
                    escola_id=escola.id,
                    created_by_user_id=professor.id
                )
                db.add(aluno)
                db.commit()
                print(f"   ✅ Aluno criado: {aluno.name}")
                print(f"      📧 Email: {aluno.email}")
                print(f"      🔑 Senha: Aluno@2024")
        else:
            print(f"   ➡️  Aluno já existe: {aluno.name}")


def criar_coordenador(db: Session, escola: Escola) -> User:
    """Cria um coordenador para a escola"""
    print("\n👔 Verificando Coordenador...")
    
    coord_email = "coordenador@escolainclusiva.com.br"
    coord = db.query(User).filter(User.email == coord_email).first()
    
    if coord:
        print(f"   ✅ Coordenador já existe: {coord.name}")
        return coord
    
    coord = User(
        name="Maria Coordenadora",
        email=coord_email,
        hashed_password=get_password_hash("Coord@2024"),
        role=UserRole.COORDINATOR,
        is_active=True,
        escola_id=escola.id
    )
    
    db.add(coord)
    db.commit()
    db.refresh(coord)
    
    print(f"   ✅ Coordenador criado: {coord.name}")
    print(f"      📧 Email: {coord_email}")
    print(f"      🔑 Senha: Coord@2024")
    
    return coord


def criar_admin_escola(db: Session, escola: Escola) -> User:
    """Cria um admin para a escola"""
    print("\n🏛️ Verificando Admin da Escola...")
    
    admin_email = "admin@escolainclusiva.com.br"
    admin = db.query(User).filter(User.email == admin_email).first()
    
    if admin:
        print(f"   ✅ Admin da Escola já existe: {admin.name}")
        return admin
    
    admin = User(
        name="João Admin",
        email=admin_email,
        hashed_password=get_password_hash("Admin@2024"),
        role=UserRole.ADMIN,
        is_active=True,
        escola_id=escola.id
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"   ✅ Admin da Escola criado: {admin.name}")
    print(f"      📧 Email: {admin_email}")
    print(f"      🔑 Senha: Admin@2024")
    
    return admin


def main():
    """Executa o setup completo"""
    print("=" * 60)
    print("🚀 SETUP INICIAL - AdaptAI")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 1. Criar Super Admin
        super_admin = criar_super_admin(db)
        
        # 2. Criar Escola
        escola = criar_escola(db)
        
        # 3. Criar Admin da Escola
        admin_escola = criar_admin_escola(db, escola)
        
        # 4. Criar Coordenador
        coordenador = criar_coordenador(db, escola)
        
        # 5. Criar Professores
        professores = criar_professores(db, escola)
        
        # 6. Associar/Criar Alunos
        associar_alunos(db, professores, escola)
        
        print("\n" + "=" * 60)
        print("✅ SETUP COMPLETO!")
        print("=" * 60)
        
        print("\n📋 RESUMO DE CREDENCIAIS:")
        print("-" * 60)
        print("🔐 SUPER ADMIN (Sistema)")
        print("   Email: admin@adaptai.com.br")
        print("   Senha: Admin@2024")
        print("   Acesso: Todo o sistema")
        print()
        print("🏛️ ADMIN DA ESCOLA")
        print("   Email: admin@escolainclusiva.com.br")
        print("   Senha: Admin@2024")
        print("   Acesso: Escola Inclusiva Modelo")
        print()
        print("👔 COORDENADOR")
        print("   Email: coordenador@escolainclusiva.com.br")
        print("   Senha: Coord@2024")
        print("   Acesso: Escola Inclusiva Modelo")
        print()
        print("👨‍🏫 PROFESSORES")
        print("   1. marcio.goes@adaptai.com.br / Prof@2024")
        print("      Alunos: Márcio Jr, Cássio")
        print("   2. fabio.azevedo@adaptai.com.br / Prof@2024")
        print("      Alunos: Enrico")
        print("   3. professor.adhoc@adaptai.com.br / Prof@2024")
        print("      ⚠️  Sem escola (Ad-Hoc)")
        print()
        print("👨‍🎓 ALUNOS")
        print("   Todos: Aluno@2024")
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
