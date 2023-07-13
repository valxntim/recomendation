import mysql.connector
import bcrypt
import streamlit as st
from PIL import Image
from io import BytesIO
from mysql.connector import Error

global cursor

def buscar_turmas():
    try:
        comando = "SELECT Id_Turma, Turma, Periodo, Nome_Professor, Horario, Disciplina_Codigo_disc, Departamento_Codigo_dep FROM Turma WHERE Turma = '01' AND Periodo = '2023.1'"
        cursor.execute(comando)
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as e:
        st.error(f"Erro ao buscar as turmas: {e}")


def excluir_estudante(matricula):
    try:
        # Remover as denúncias de professor associadas ao estudante
        comando = "DELETE FROM DenunciaAvProf WHERE AvaliaProf_idAvaliaProf IN (SELECT idAvaliaProf FROM AvaliaProf WHERE Estudante_Matricula = %s)"
        valores = (matricula,)
        cursor.execute(comando, valores)
        conexao.commit()

        # Remover as avaliações associadas ao estudante
        comando = "DELETE FROM AvaliaProf WHERE Estudante_Matricula = %s"
        valores = (matricula,)
        cursor.execute(comando, valores)
        conexao.commit()

        # Remover as denúncias de turma associadas ao estudante
        comando = "DELETE FROM DenunciaAvTurma WHERE Estudante_Matricula = %s"
        valores = (matricula,)
        cursor.execute(comando, valores)
        conexao.commit()

        # Remover as avaliações associadas ao estudante
        comando = "DELETE FROM AvaliaTurma WHERE Estudante_Matricula = %s"
        valores = (matricula,)
        cursor.execute(comando, valores)
        conexao.commit()

        # Remover o estudante
        comando = "DELETE FROM Estudante WHERE Matricula = %s"
        valores = (matricula,)
        cursor.execute(comando, valores)
        conexao.commit()

        st.success("Estudante excluído com sucesso!")
    except mysql.connector.Error as e:
        st.error(f"Erro ao excluir o estudante: {e}")


def remover_avaliacao(id_avaliacao):
    try:
        # Remover as denúncias associadas à avaliação
        comando = "DELETE FROM DenunciaAvProf WHERE AvaliaProf_IdAvaliaProf = %s"
        valores = (id_avaliacao,)
        cursor.execute(comando, valores)
        conexao.commit()

        # Remover a avaliação
        comando = "DELETE FROM AvaliaProf WHERE IdAvaliaProf = %s"
        valores = (id_avaliacao,)
        cursor.execute(comando, valores)
        conexao.commit()

        st.success("Avaliação removida com sucesso!")
    except mysql.connector.Error as e:
        st.error(f"Erro ao remover a avaliação: {e}")



def inserir_avaliacao(matricula, id_professor, avaliacao, score):
    try:
        comando = "INSERT INTO AvaliaProf (Estudante_Matricula, Professor_Id_Professor, Texto, Score) VALUES (%s, %s, %s, %s)"
        valores = (matricula, id_professor, avaliacao, score)
        cursor.execute(comando, valores)
        conexao.commit()
        st.success("Avaliação registrada com sucesso!")
    except Error as e:
        st.error(f"Erro ao inserir a avaliação: {e}")

def remover_denuncia_turma(id_avaliacao):
    try:
        comando = "DELETE FROM DenunciaAvTurma WHERE AvaliaTurma_IdAvaliaTurma = %s"
        valores = (id_avaliacao,)
        cursor.execute(comando, valores)
        conexao.commit()
    except Error as e:
        st.error(f"Erro ao remover a denúncia de turma: {e}")

def buscar_denuncias_turma():
    comando = "SELECT AvaliaTurma_IdAvaliaTurma, Estudante_Matricula, Texto, Score FROM DenunciaAvTurma"
    cursor.execute(comando)
    resultados = cursor.fetchall()
    return resultados


def buscar_denuncias_professor():
    comando = "SELECT AvaliaProf_IdAvaliaProf FROM DenunciaAvProf"
    cursor.execute(comando)
    resultados = cursor.fetchall()
    return resultados

def buscar_avaliacao_por_id(id_avaliacao):
    comando = "SELECT Estudante_Matricula, Texto, Score FROM AvaliaProf WHERE IdAvaliaProf = %s"
    valores = (id_avaliacao,)
    cursor.execute(comando, valores)
    resultado = cursor.fetchone()
    return resultado


def exibir_avaliacoes_denunciadas_professor():
    denuncias = buscar_denuncias_professor()
    if len(denuncias) > 0:
        st.subheader("Avaliações de Professor Denunciadas")
        for denuncia in denuncias:
            id_avaliacao = denuncia[0]
            # Buscar avaliação com base no ID da avaliação
            avaliacao = buscar_avaliacao_por_id(id_avaliacao)
            if avaliacao is not None:
                matricula = avaliacao[1]
                texto = avaliacao[2]
                score = avaliacao[3]
                st.write("ID da Avaliação:", id_avaliacao)
                st.write("Matrícula do Estudante:", matricula)
                st.write("Avaliação:", texto)
                st.write("Pontuação:", score)

                # Botão de remoção da denúncia
                if st.button("Remover Denúncia de Professor", key=f"remover_denuncia_professor_{id_avaliacao}"):
                    remover_denuncia_professor(id_avaliacao)
                    st.success("Denúncia de professor removida com sucesso!")

                st.write("----------")
    else:
        st.info("Nenhuma denúncia encontrada para feedback de professor.")

def remover_denuncia_professor(id_avaliacao):
    try:
        comando = "DELETE FROM DenunciaAvProf WHERE AvaliaProf_IdAvaliaProf = %s"
        valores = (id_avaliacao,)
        cursor.execute(comando, valores)
        conexao.commit()
    except Error as e:
        st.error(f"Erro ao remover a denúncia de professor: {e}")

def is_admin(matricula):
    comando = "SELECT IsAdmin FROM Estudante WHERE Matricula = %s"
    valores = (matricula,)
    cursor.execute(comando, valores)
    resultado = cursor.fetchone()

    if resultado is not None:
        is_admin = resultado[0]
        return is_admin
    return False

def denunciar_avaliacao_professor(id_avaliacao, matricula_denunciante):
    try:
        comando = "INSERT INTO DenunciaAvProf (AvaliaProf_IdAvaliaProf, Estudante_Matricula) VALUES (%s, %s)"
        valores = (id_avaliacao, matricula_denunciante)
        cursor.execute(comando, valores)
        conexao.commit()
        st.success("Avaliação de professor denunciada com sucesso!")
    except mysql.connector.Error as e:
        st.error(f"Erro ao denunciar a avaliação de professor: {e}")

def denunciar_avaliacao_turma(id_avaliacao, matricula_denunciante):
    try:
        comando = "INSERT INTO DenunciaAvTurma (AvaliaTurma_IdAvaliaTurma, Estudante_Matricula) VALUES (%s, %s)"
        valores = (id_avaliacao, matricula_denunciante)
        cursor.execute(comando, valores)
        conexao.commit()
        st.success("Avaliação de turma denunciada com sucesso!")
    except mysql.connector.Error as e:
        st.error(f"Erro ao denunciar a avaliação de turma: {e}")

def exibir_avaliacoes_professor(id_professor):
    try:
        comando = "SELECT IdAvaliaProf, Estudante_Matricula, Texto, Score FROM AvaliaProf WHERE Professor_Id_Professor = %s"
        valores = (id_professor,)
        cursor.execute(comando, valores)
        resultados = cursor.fetchall()
        if len(resultados) > 0:
            st.subheader("Avaliações do Professor")
            for resultado in resultados:
                id_avaliacao = resultado[0]
                matricula = resultado[1]
                texto = resultado[2]
                score = resultado[3]
                st.write("Matrícula do Estudante:", matricula)
                st.write("Avaliação:", texto)
                st.write("Pontuação:", score)

                # Botão de denúncia
                if st.button("Denunciar Avaliação de Professor", key=f"denunciar_professor_{id_avaliacao}"):
                    # Obtém a matrícula do usuário logado
                    matricula_denunciante = matricula
                    denunciar_avaliacao_professor(id_avaliacao, matricula_denunciante)

                st.write("----------")
        else:
            st.info("Nenhuma avaliação encontrada para este professor.")
    except mysql.connector.Error as e:
        st.error(f"Erro ao buscar as avaliações do professor: {e}")

def exibir_avaliacoes_turma(id_turma):
    try:
        comando = "SELECT IdAvaliaTurma, Estudante_Matricula, Texto, Score FROM AvaliaTurma WHERE Turma_Id_Turma = %s"
        valores = (id_turma,)
        cursor.execute(comando, valores)
        resultados = cursor.fetchall()
        if len(resultados) > 0:
            st.subheader("Avaliações da Turma")
            for resultado in resultados:
                id_avaliacao = resultado[0]
                matricula = resultado[1]
                texto = resultado[2]
                score = resultado[3]
                st.write("Matrícula do Estudante:", matricula)
                st.write("Avaliação:", texto)
                st.write("Pontuação:", score)

                # Botão de denúncia
                if st.button("Denunciar Avaliação de Turma", key=f"denunciar_turma_{id_avaliacao}"):
                    # Obtém a matrícula do usuário logado
                    matricula_denunciante = st.experimental_get_query_params()["matricula"][0]
                    denunciar_avaliacao_turma(id_avaliacao, matricula_denunciante)

                st.write("----------")
        else:
            st.info("Nenhuma avaliação encontrada para esta turma.")
    except mysql.connector.Error as e:
        st.error(f"Erro ao buscar as avaliações da turma: {e}")

def inserir_avaliacao_professor(matricula, id_professor, avaliacao, score):
    try:
        comando = "INSERT INTO AvaliaProf (Estudante_Matricula, Professor_Id_Professor, Texto, Score) VALUES (%s, %s, %s, %s)"
        valores = (matricula, id_professor, avaliacao, score)
        cursor.execute(comando, valores)
        conexao.commit()
        st.success("Avaliação de professor registrada com sucesso!")
    except mysql.connector.Error as e:
        st.error(f"Erro ao inserir a avaliação de professor: {e}")

def inserir_avaliacao_turma(matricula, id_turma, avaliacao, score):
    try:
        comando = "INSERT INTO AvaliaTurma (Estudante_Matricula, Turma_Id_Turma, Texto, Score) VALUES (%s, %s, %s, %s)"
        valores = (matricula, id_turma, avaliacao, score)
        cursor.execute(comando, valores)
        conexao.commit()
        st.success("Avaliação de turma registrada com sucesso!")
    except mysql.connector.Error as e:
        st.error(f"Erro ao inserir a avaliação de turma: {e}")

def buscar_professores():
    comando = "SELECT Id_Professor, Turma_Nome_Professor FROM Professor"
    cursor.execute(comando)
    resultados = cursor.fetchall()
    return resultados

def buscar_login(matricula):
    comando = "SELECT Login FROM Estudante WHERE Matricula = %s"
    valores = (matricula,)
    cursor.execute(comando, valores)
    resultado = cursor.fetchone()

    if resultado is not None:
        login = resultado[0]
        return login
    return None

def buscar_email(matricula):
    comando = "SELECT Email FROM Estudante WHERE Matricula = %s"
    valores = (matricula,)
    cursor.execute(comando, valores)
    resultado = cursor.fetchone()

    if resultado is not None:
        email = resultado[0]
        return email
    return None

def buscar_curso(matricula):
    comando = "SELECT Curso FROM Estudante WHERE Matricula = %s"
    valores = (matricula,)
    cursor.execute(comando, valores)
    resultado = cursor.fetchone()

    if resultado is not None:
        curso = resultado[0]
        return curso
    return None

def excluir_imagem_perfil(matricula):
    comando = "UPDATE Estudante SET Imagem = NULL WHERE Matricula = %s"
    valores = (matricula,)
    cursor.execute(comando, valores)
    conexao.commit()

def buscar_imagem_perfil(matricula):
    comando = "SELECT Imagem FROM Estudante WHERE Matricula = %s"
    valores = (matricula,)
    cursor.execute(comando, valores)
    resultado = cursor.fetchone()

    if resultado is not None:
        imagem = resultado[0]
        return imagem
    return None

def atualizar_imagem_perfil(matricula, nova_imagem_bytes):
    comando = "UPDATE Estudante SET Imagem = %s WHERE Matricula = %s"
    valores = (nova_imagem_bytes, matricula)
    cursor.execute(comando, valores)
    conexao.commit()

def atualizar_login(matricula, novo_login):
    comando = "UPDATE Estudante SET Login = %s WHERE Matricula = %s"
    valores = (novo_login, matricula)
    cursor.execute(comando, valores)
    conexao.commit()

def atualizar_email(matricula, novo_email):
    comando = "UPDATE Estudante SET Email = %s WHERE Matricula = %s"
    valores = (novo_email, matricula)
    cursor.execute(comando, valores)
    conexao.commit()

def atualizar_senha(matricula, nova_senha):
    # Criptografar a nova senha
    senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    comando = "UPDATE Estudante SET Senha = %s WHERE Matricula = %s"
    valores = (senha_hash, matricula)
    cursor.execute(comando, valores)
    conexao.commit()

def atualizar_curso(matricula, novo_curso):
    comando = "UPDATE Estudante SET Curso = %s WHERE Matricula = %s"
    valores = (novo_curso, matricula)
    cursor.execute(comando, valores)
    conexao.commit()

def verificar_login(matricula, senha):
    # Consultar o banco de dados para verificar se a matrícula existe
    comando = "SELECT Senha FROM Estudante WHERE Matricula = %s"
    valores = (matricula,)
    cursor.execute(comando, valores)
    resultado = cursor.fetchone()

    if resultado is not None:
        senha_hash = resultado[0].encode('utf-8')
        # Verificar se a senha fornecida corresponde à senha armazenada no banco de dados
        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
            return True
    return False

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='@Gustavo10@',
    database='mydb',
)

cursor = conexao.cursor()

def main():
    st.title("Feedback UNB")

    # Obtém o status de login e informações adicionais a partir do cookie
    user_info = st.session_state.get('user_info', {'logged_in': False, 'is_admin': False})

    # Definir a variável de sessão user_info se ainda não estiver definida
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = {'logged_in': False, 'is_admin': False}

    option = st.sidebar.selectbox("Selecione a operação", ("Cadastrar Usuário", "Login", "Turmas", "Professores", "Configurações", "Denúncias", "Sair"))


    if option == "Denúncias":
        if user_info['logged_in'] and user_info['is_admin']:
            st.subheader("Denúncias")
            st.markdown("Selecione o tipo de denúncia:")
            denuncia_option = st.radio("Tipo de Denúncia", ("Feedback de Professor", "Feedback de Turma"))

            if denuncia_option == "Feedback de Professor":
                denuncias = buscar_denuncias_professor()
                if len(denuncias) > 0:
                    st.subheader("Avaliações de Professor Denunciadas")
                    for denuncia in denuncias:
                        id_avaliacao = denuncia[0]
                        st.write("ID da Avaliação:", id_avaliacao)

                        # Buscar detalhes da avaliação
                        avaliacao = buscar_avaliacao_por_id(id_avaliacao)
                        if avaliacao is not None:
                            matricula = avaliacao[0]
                            texto = avaliacao[1]
                            score = avaliacao[2]

                            st.write("Matrícula do Estudante:", matricula)
                            st.write("Avaliação:", texto)
                            st.write("Pontuação:", score)

                        # Botão de remoção da denúncia
                        if st.button("Descartar Denúncia de Professor", key=f"remover_denuncia_professor_{id_avaliacao}"):
                            remover_denuncia_professor(id_avaliacao)
                            st.success("Denúncia de professor removida com sucesso!")

                        # Botão de remoção da avaliação
                        if st.button("Remover Avaliação", key=f"remover_avaliacao_{id_avaliacao}"):
                            remover_avaliacao(id_avaliacao)
                            st.success("Avaliação removida com sucesso!")

                        # Botão de remoção do estudante
                        if st.button("Excluir Estudante", key=f"excluir_estudante_{matricula}"):
                            excluir_estudante(matricula)
                            st.success("Estudante excluído com sucesso!")

                        st.write("----------")
                else:
                    st.info("Nenhuma denúncia encontrada para feedback de professor.")

            elif denuncia_option == "Feedback de Turma":
                denuncias = buscar_denuncias_turma()
                if len(denuncias) > 0:
                    st.subheader("Avaliações de Turma Denunciadas")
                    for denuncia in denuncias:
                        id_avaliacao = denuncia[0]
                        matricula = denuncia[1]
                        texto = denuncia[2]
                        score = denuncia[3]
                        st.write("Matrícula do Estudante:", matricula)
                        st.write("Avaliação:", texto)
                        st.write("Pontuação:", score)

                        # Botão de remoção da denúncia
                        if st.button("Remover Denúncia de Turma", key=f"remover_denuncia_turma_{id_avaliacao}"):
                            remover_denuncia_turma(id_avaliacao)
                            st.success("Denúncia de turma removida com sucesso!")

                        # Botão de remoção do estudante
                        if st.button("Excluir Estudante", key=f"excluir_estudante_{matricula}"):
                            excluir_estudante(matricula)
                            st.success("Estudante excluído com sucesso!")

                        st.write("----------")
                else:
                    st.info("Nenhuma denúncia encontrada para feedback de turma.")

        else:
            st.warning("Você não tem permissão para acessar esta página de denúncias.")


    elif option == "Login":
        if not user_info['logged_in']:
            st.subheader("Login")

            matricula = st.text_input("Matrícula",max_chars=9)
            senha = st.text_input("Senha", type="password")

            if st.button("Entrar"):
                if verificar_login(matricula, senha):
                    # Armazena o status de login no cookie
                    user_info['logged_in'] = True
                    user_info['matricula'] = matricula
                    user_info['is_admin'] = is_admin(matricula)
                    st.success("Login bem-sucedido! Você está logado no sistema.")
                else:
                    st.error("Matrícula ou senha incorretas. Tente novamente.")

    elif option == "Turmas":
        if user_info['logged_in']:
            st.subheader("Turmas")
            turmas = buscar_turmas()

            if not turmas:
                st.warning("Nenhuma turma encontrada com os critérios fornecidos.")
            else:
                # Adicione campos de entrada para coletar informações do usuário
                nome_professor = st.text_input("Nome do Professor")

                # Filtra as turmas com base no nome do professor fornecido pelo usuário
                turmas_filtradas = []
                for turma in turmas:
                    if turma[3] == nome_professor:
                        turmas_filtradas.append(turma)

                if not turmas_filtradas:
                    st.warning("Nenhuma turma encontrada com o professor fornecido.")
                else:
                    # Itera sobre as turmas filtradas e exibe as informações de cada uma delas
                    for turma in turmas_filtradas:
                        id_turma = turma[0]
                        nome_turma = turma[1]
                        st.write("ID da Turma:", id_turma)
                        st.write("Nome da Turma:", nome_turma)

                        # Exibe as avaliações para a turma selecionada
                        exibir_avaliacoes_turma(id_turma)

                        # Adicione a caixa de texto para a avaliação
                        avaliacao = st.text_area("Avaliação")

                        # Adicione o controle deslizante (slider) para a pontuação
                        score = st.slider("Pontuação", min_value=0, max_value=5, step=1)

                        # Adicione um botão para enviar a avaliação
                        if st.button("Enviar Avaliação"):
                            # Obtém a matrícula do usuário logado
                            matricula = st.experimental_get_query_params()["matricula"][0]

                            # Insere a avaliação e a pontuação no banco de dados
                            inserir_avaliacao_turma(matricula, id_turma, avaliacao, score)

            # Resto do código para a tela de Turmas acessível apenas para usuários logados
        else:
            st.warning("Você precisa fazer login para acessar esta tela.")





    elif option == "Professores":
        if user_info['logged_in']:
            st.subheader("Professores")
            professores = buscar_professores()
            nomes_professores = [professor[1] for professor in professores]
            nome_professor = st.selectbox("Selecione um professor", nomes_professores)
            id_professor = None
            for professor in professores:
                if professor[1] == nome_professor:
                    id_professor = professor[0]
                    break
            st.write("ID do Professor:", id_professor)  # Exibido apenas para fins de depuração, pode ser removido

            # Exibe as avaliações para o professor selecionado
            exibir_avaliacoes_professor(id_professor)

            # Adicione a caixa de texto para a avaliação
            avaliacao = st.text_area("Avaliação")

            # Adicione o controle deslizante (slider) para a pontuação
            score = st.slider("Pontuação", min_value=0, max_value=5, step=1)

            # Adicione um botão para enviar a avaliação
            if st.button("Enviar Avaliação"):
                # Obtém a matrícula do usuário logado
                #matricula = st.experimental_get_query_params()["matricula"][0]
                matricula = user_info['matricula']


                # Insere a avaliação e a pontuação no banco de dados
                inserir_avaliacao(matricula, id_professor, avaliacao, score)

            # Resto do código para a tela de Professores acessível apenas para usuários logados
        else:
            st.warning("Você precisa fazer login para acessar esta tela.")


    elif option == "Configurações":
        if user_info['logged_in']:
            st.subheader("Configurações")

            # Obtém a matrícula do usuário logado
            matricula = user_info['matricula']
            st.markdown("Sua Matrícula: " + matricula)

            login = buscar_login(matricula)
            if login is not None:
                novo_login = st.text_input("Novo Login", value=login)
                if st.button("Salvar Login"):
                    atualizar_login(matricula, novo_login)
                    st.success("Login atualizado com sucesso!")

            email = buscar_email(matricula)
            if email is not None:
                novo_email = st.text_input("Novo Email", value=email)
                if st.button("Salvar Email"):
                    atualizar_email(matricula, novo_email)
                    st.success("Email atualizado com sucesso!")

            senha = st.text_input("Nova Senha", type="password")
            if st.button("Salvar Senha"):
                atualizar_senha(matricula, senha)
                st.success("Senha atualizada com sucesso!")

            curso = buscar_curso(matricula)
            if curso is not None:
                novo_curso = st.text_input("Novo Curso", value=curso)
                if st.button("Salvar Curso"):
                    atualizar_curso(matricula, novo_curso)
                    st.success("Curso atualizado com sucesso!")

            # Busca a imagem de perfil do usuário
            imagem_perfil = buscar_imagem_perfil(matricula)

            # Exibe a imagem de perfil, se encontrada
            if imagem_perfil is not None:
                imagem_b = BytesIO(imagem_perfil)
                imagem = Image.open(imagem_b)
                tamanho_desejado=(200,200)
                imagem_redimensionada = imagem.resize(tamanho_desejado)
                st.image(imagem_redimensionada, caption="Foto de Perfil")

            # Componente de upload de arquivo para permitir a seleção de uma nova imagem
            nova_imagem = st.file_uploader("Alterar Imagem de Perfil", type=["jpg", "jpeg", "png"])

            if nova_imagem is not None:
                # Limitar o tamanho da imagem a 2 MB
                nova_imagem_bytes = nova_imagem.read(2 * 1024 * 1024)

                # Atualizar a imagem de perfil no banco de dados
                atualizar_imagem_perfil(matricula, nova_imagem_bytes)
                st.success("Imagem de perfil atualizada com sucesso!")

            # Botão para excluir a foto de perfil
            if st.button("Excluir Foto"):
                excluir_imagem_perfil(matricula)
                st.success("Foto de perfil excluída com sucesso!")

        else:
            st.warning("Você precisa fazer login para acessar esta tela.")

    elif option == "Sair":
        if user_info['logged_in']:
            # Remove o status de login do cookie
            user_info['logged_in'] = False
            st.experimental_set_query_params(logged_in=False)
            st.info("Você saiu do sistema.")
        else:
            st.warning("Você não está logado.")

    elif option == "Cadastrar Usuário":
        if not user_info['logged_in']:
            st.subheader("Criar Usuário")
            matricula = st.text_input("Inserir Matrícula", max_chars=9)
            senha = st.text_input("Inserir Senha", type="password")  # Campo de senha oculto
            login = st.text_input("Login")
            email = st.text_input("Inserir Email")
            curso = st.text_input("Inserir Curso")
            foto = st.file_uploader("Inserir Foto de Perfil", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
            if st.button("Create"):
                # Criptografar a senha
                senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                # Verificar se uma foto foi fornecida
                if foto is not None:
                    # Limitar o tamanho da imagem a 2 MB
                    foto_bytes = foto.read(2 * 1024 * 1024)

                    # Inserir os dados na tabela Aluno, incluindo a foto
                    comando = "INSERT INTO Estudante (Matricula, Senha, Login, Email, Curso, Imagem) VALUES (%s, %s, %s, %s, %s, %s)"
                    valores = (matricula, senha_hash, login, email, curso, foto_bytes)
                    cursor.execute(comando, valores)
                    conexao.commit()  # Editar o banco de dados
                    st.success("Usuário criado com sucesso!")

                    # Redirecionar o usuário para a tela de login
                    st.experimental_set_query_params(create_success=True)
                else:
                    # Inserir os dados na tabela Aluno, sem a foto
                    comando = "INSERT INTO Estudante (Matricula, Senha, Login, Email, Curso) VALUES (%s, %s, %s, %s, %s)"
                    valores = (matricula, senha_hash, login, email, curso)
                    cursor.execute(comando, valores)
                    conexao.commit()  # Editar o banco de dados
                    st.success("Usuário criado com sucesso!")

                    # Redirecionar o usuário para a tela de login
                    st.experimental_set_query_params(create_success=True)


if __name__ == "__main__":
    main()
