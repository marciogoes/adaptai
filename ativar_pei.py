# Ativar todos os PEIs do aluno Marcio
import pymysql

conn = pymysql.connect(
    host="teamarcionovo.mysql.dbaas.com.br",
    user="teamarcionovo",
    password="MarcioGo1003@@",
    database="teamarcionovo",
    port=3306
)

cursor = conn.cursor()

# Ver PEIs
cursor.execute("SELECT id, student_id, status, ano_letivo FROM peis ORDER BY id DESC LIMIT 5")
print("PEIs existentes:")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, Student: {row[1]}, Status: {row[2]}, Ano: {row[3]}")

# Ativar
cursor.execute("UPDATE peis SET status = 'ativo' WHERE student_id = 1")
conn.commit()
print(f"\n✅ {cursor.rowcount} PEI(s) ativado(s) para o aluno Marcio!")

conn.close()
