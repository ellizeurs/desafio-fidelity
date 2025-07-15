import datetime
import mariadb
import sys
import os
import time
from tqdm import tqdm
from .platforms.tjsp import TJSPConsulta

from src.consts import (
    NADA_CONSTA,
    CONSTA01,
    CONSTA02,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
)


class SPVAutomatico:

    def __init__(self, filtro="", platforma=TJSPConsulta()):
        self.filtro = filtro
        self.conn = None
        self.platforma = platforma

    # Esse método inicia o sistema e consulta as pesquisas que estão em aberto no banco de dados.
    def conectaBD(self, filtro, pagina=0, limite=210):
        if self.conn is None:
            self.conn = mariadb.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
            )
        cursor = self.conn.cursor()
        cond = ""
        offset = pagina * limite
        if filtro == 1 or filtro == 3:
            cond = ' AND rg <> "" '

        sql = (
            "SELECT DISTINCT p.Cod_Cliente, p.Cod_Pesquisa,  e.UF, p.Data_Entrada, coalesce(p.nome_corrigido, p.nome) AS Nome, p.CPF, coalesce(p.rg_corrigido, p.rg) AS RG, p.Nascimento, coalesce(p.mae_corrigido, p.mae) AS Mae, p.anexo AS Anexo, ps.Resultado, ps.cod_spv_tipo FROM pesquisa p INNER JOIN servico s ON p.Cod_Servico = s.Cod_Servico LEFT JOIN lote_pesquisa lp ON p.Cod_Pesquisa = lp.Cod_Pesquisa LEFT JOIN lote l ON l.cod_lote = lp.cod_lote LEFT JOIN estado e ON e.Cod_UF = p.Cod_UF LEFT JOIN pesquisa_spv ps ON ps.Cod_Pesquisa = p.Cod_Pesquisa AND ps.Cod_SPV = 1 AND ps.filtro = "
            + str(filtro)
            + ' WHERE p.Data_Conclusao IS NULL  AND ps.resultado IS NULL   AND p.tipo = 0   AND p.cpf <> "" '
            + cond
            + ' AND (e.UF = "SP" OR p.Cod_UF_Nascimento = 26  OR p.Cod_UF_RG = 26) GROUP BY p.cod_pesquisa ORDER BY nome ASC, resultado DESC '
            + f"LIMIT {limite} OFFSET {offset}"
        )

        cursor.execute(sql)

        qry = cursor.fetchall()

        cursor.close()
        return qry

    # Esse método possui a função de consultar a pesquisa no banco de dados e executá-la utilizando a biblioteca Selenoid.
    # A parte da execução é aplicada utilizando o método executaPesquisa().
    def pesquisa(self):
        w = 0
        tempo_inicio = datetime.datetime.now()

        filtro = self.filtro
        i = self.filtro
        qry = self.conectaBD(filtro)

        totPesquisas = len(qry)
        if totPesquisas > 0:

            for dados in tqdm(qry):
                codPesquisa = dados[1]
                nome = dados[4]
                cpf = dados[5]
                rg = dados[6]
                spvTipo = dados[11]

                self.executaPesquisa(self, filtro, nome, cpf, rg, codPesquisa, spvTipo)
                tempo_fim = datetime.datetime.now()
                tempo_gasto = round((tempo_fim - tempo_inicio).total_seconds(), 2)
                if tempo_gasto >= 600:
                    break

            tempo_gasto = 0
            i = i + 1
            if i <= 3:
                print("RECOMENÇANDO COM O FILTRO " + str(i))
                p = SPVAutomatico(i)
                p.pesquisa()
            else:
                print("RECOMEÇANDO")
                self.restarta_programa(self)
        else:

            # TENTA COM O PRÓXIMO FILTRO

            w = w + 1
            print("AGUARDANDO PARA RECOMEÇAR")
            time.sleep(60)
            if w >= 20:
                time.sleep(3600)
                self.restarta_programa(self)
            else:
                self.restarta_programa(self)

    # Esse método tem como função realizar todos os passos da pesquisa, após a sua consulta no banco de dados.
    # Com isso é realizada a busca no navegador, a validação do resultado e a inserção do resultado no banco de dados.
    def executaPesquisa(self, filtro, nome, cpf, rg, codPesquisa, spvTipo):

        if filtro == 0 and cpf != None:
            site = self.carregaSite(self, filtro, cpf)
            result = self.checaResultado(site, codPesquisa)
            sql = (
                "insert into pesquisa_spv (Cod_Pesquisa, Cod_SPV, Cod_spv_computador, Cod_Spv_Tipo, Resultado, Cod_Funcionario, filtro, website_id) values ("
                + str(codPesquisa)
                + ", 1, 36, NULL, "
                + str(result)
                + ", -1, "
                + str(filtro)
                + ", 1)"
            )

        elif filtro in [1, 3] and rg != None and rg != "":
            site = self.carregaSite(self, filtro, rg)
            result = self.checaResultado(site, codPesquisa)
            sql = (
                "insert into pesquisa_spv (Cod_Pesquisa, Cod_SPV, Cod_spv_computador, Cod_Spv_Tipo, Resultado, Cod_Funcionario, filtro, website_id) values ("
                + str(codPesquisa)
                + ", 1, 36, NULL, "
                + str(result)
                + ", -1, "
                + str(filtro)
                + ", 1)"
            )

        elif filtro == 2 and nome != None and nome != "":
            site = self.carregaSite(self, filtro, nome)
            result = self.checaResultado(site, codPesquisa)
            sql = (
                "insert into pesquisa_spv (Cod_Pesquisa, Cod_SPV, Cod_spv_computador, Cod_Spv_Tipo, Resultado, Cod_Funcionario, filtro, website_id) values ("
                + str(codPesquisa)
                + ", 1, 36, NULL, "
                + str(result)
                + ", -1, "
                + str(filtro)
                + ", 1)"
            )
        if self.conn is None:
            self.conn = mariadb.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
            )
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()

    # Esse método tem como função enquadrar a pesquisa de acordo com o resultado obtido na pesquisa como Nada Consta, Consta
    # Criminal e Consta Cível.
    @staticmethod
    def checaResultado(site, codPesquisa):
        final_result = 7
        if NADA_CONSTA in site:
            final_result = 1
        elif ((CONSTA01 in site) or (CONSTA02 in site)) and (
            ("Criminal" in site) or ("criminal" in site)
        ):
            final_result = 2
        elif (CONSTA01 in site) or (CONSTA02 in site):
            final_result = 5

        return final_result

    # Esse método tem como função buscar a pesquisa na plataforma online utilizando o Selenoid.
    def carregaSite(self, filtro, documento):
        try:
            return self.plataforma.consultar(documento, filtro)
        except Exception as e:
            self.restarta_programa(self)

    # Esse método tem como função reiniciar o sistema.
    def restarta_programa(self):
        try:
            if self.conn:
                self.conn.close()
            python = sys.executable
            os.execl(python, python, *sys.argv)
        except:
            print("PROGRAMA ENCERRADO")
            quit()
