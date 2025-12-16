import pandas as pd
import os
# Demander à l'utilisateur le chemin du fichier Excel
excel_file = input("Entrez le chemin complet de votre fichier Excel : ")
sheet_name = "Ma Feuille"
table_name = input("Entrez le nom de la table SQL à créer : ")

# Si l'utilisateur ne met pas de nom de feuille, prendre la première
if sheet_name.strip() == "":
    sheet_name = 0

# Lire le fichier Excel
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Générer le script CREATE TABLE (tout en TEXT pour simplifier)
create_table_sql = f"CREATE TABLE {table_name} (\n"
for col in df.columns:
    create_table_sql += f"    {col} TEXT,\n"
create_table_sql = create_table_sql.rstrip(',\n') + "\n);\n\n"

# Générer les INSERT INTO pour chaque ligne
insert_sql = ""
for _, row in df.iterrows():
    values = []
    for val in row:
        if pd.isna(val):
            values.append("NULL")
        else:
            # Échappe les quotes simples
            values.append(f"'{str(val).replace('\'','\'\'')}'")
    insert_sql += f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(values)});\n"

# Écrire le script SQL dans un fichier
sql_file = table_name+".sql"
with open(sql_file, 'w', encoding='utf-8') as f:
    f.write(create_table_sql)
    f.write(insert_sql)

print("Fichier créé ici :", os.path.abspath(sql_file))

