/* vim:ts=4:et:ai:si:sw=4:tw=80
 *
 * Locadora de video
 *
 * Copyright 2006, Osvaldo Santana Neto <osantana.spam@gmail.com>
 * Dominio Publico. As notas de copyright podem ser omitidas.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ENTRY 500
#define MAX_MENU_ENTRY 5

/* Filme */
typedef struct {
    char nome[50];
    char genero[50];
    char ano[4];
    char disponivel;
} filme_t;

typedef struct _elemento_filme_t {
    long id;
    filme_t *filme;
    struct _elemento_filme_t *proximo;
} elemento_filme_t;

typedef struct {
    char nome[50];
    char endereco[100];
    char telefone[20];
    char alugados;
} cliente_t;

/* Cliente */
typedef struct _elemento_cliente_t {
    long id;
    cliente_t *cliente;
    struct _elemento_cliente_t *proximo;
} elemento_cliente_t;

typedef struct {
    FILE *arquivo_filmes;
    elemento_filme_t *filmes;
    elemento_filme_t *ultimo_filme;

    FILE *arquivo_clientes;
    elemento_cliente_t *clientes;
    elemento_cliente_t *ultimo_cliente;
} cadastro_t;

/* Prototipos */
void clrscr(void);
void remove_linebreak(char *s);

/* Filmes */
void cadastra_filme(cadastro_t *cadastro);
elemento_filme_t *consulta_filme(cadastro_t *cadastro);

void inclui_filme(cadastro_t *cadastro, filme_t *filme, int grava_arquivo);
void registra_locacao_filme(cadastro_t *cadastro, elemento_filme_t
                            *elemento_filme, char disponivel);
elemento_filme_t *pesquisa_filme(cadastro_t *cadastro, const char *nome);

/* Clientes */
void cadastra_cliente(cadastro_t *cadastro);
elemento_cliente_t *consulta_cliente(cadastro_t *cadastro);

void inclui_cliente(cadastro_t *cadastro, cliente_t *cliente, int
                    grava_arquivo);
void registra_locacao_cliente(cadastro_t *cadastro, elemento_cliente_t
                              *elemento_cliente, char disponivel);
elemento_cliente_t *pesquisa_cliente(cadastro_t *cadastro, const char *nome);

/* Locacao */
void loca_filme(cadastro_t *cadastro);
void devolve_filme(cadastro_t *cadastro);

/* Implementacao */
void
clrscr(void)
{
#ifndef DEBUG
    fprintf(stdout, "\033[2J");
    fprintf(stdout, "\033[1;1H");
#endif
}

void
remove_linebreak(char *s)
{
    char *linebreak;
    if ( linebreak = strchr(s, '\r') ) *linebreak = '\0';
    if ( linebreak = strchr(s, '\n') ) *linebreak = '\0';
}



/* Filmes */
void
cadastra_filme(cadastro_t *cadastro)
{
    filme_t *filme;
    long id = 0;
    char entrada[MAX_ENTRY];

    if (!(filme = (filme_t *) malloc(sizeof(filme_t)))) {
        return;
    }

    clrscr();
    printf("Cadastro filme\n");
    printf("==============\n\n");

    memset(entrada, 0, MAX_ENTRY);
    printf("Nome:   "); fgets(entrada, MAX_ENTRY, stdin);
    remove_linebreak(entrada);
    strncpy(filme->nome, entrada, 50);

    if (pesquisa_filme(cadastro, filme->nome)) {
        printf("Filme ja cadastrado! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }

    memset(entrada, 0, MAX_ENTRY);
    printf("Genero: "); fgets(entrada, MAX_ENTRY, stdin);
    remove_linebreak(entrada);
    strncpy(filme->genero, entrada, 50);

    memset(entrada, 0, MAX_ENTRY);
    printf("Ano:    "); fgets(entrada, MAX_ENTRY, stdin);
    remove_linebreak(entrada);
    strncpy(filme->ano, entrada, 4);

    filme->disponivel = 1;

    inclui_filme(cadastro, filme, 1);
}

elemento_filme_t *
consulta_filme(cadastro_t *cadastro)
{
    elemento_filme_t *elemento_filme;
    long id = 0;
    char entrada[MAX_ENTRY];

    memset(entrada, 0, MAX_ENTRY);
    printf("Nome:       "); fgets(entrada, MAX_ENTRY, stdin);
    remove_linebreak(entrada);
    if (! (elemento_filme = pesquisa_filme(cadastro, entrada))) {
        printf("Filme nao encontrado! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return NULL;
    }

    printf("Genero:     %s\n", elemento_filme->filme->genero);
    printf("Ano:        %s\n", elemento_filme->filme->ano);
    printf("Disponivel: %s\n",
        (elemento_filme->filme->disponivel) ? "sim" : "nao");
    return elemento_filme;
}


void
inclui_filme(cadastro_t *cadastro, filme_t *filme, int grava_arquivo)
{
    elemento_filme_t *elemento_filme;

    elemento_filme = (elemento_filme_t *)malloc(sizeof(elemento_filme_t));

    if (cadastro->ultimo_filme) {
        elemento_filme->id = cadastro->ultimo_filme->id + 1;
        cadastro->ultimo_filme->proximo = elemento_filme;
    } else {
        elemento_filme->id = 0;
    }

    elemento_filme->filme = filme;
    elemento_filme->proximo = NULL;

    if (!cadastro->filmes) cadastro->filmes = elemento_filme;
    cadastro->ultimo_filme = elemento_filme;

#ifdef DEBUG
    printf("incluido filme '%s'\n", elemento_filme->filme->nome);
#endif

    if (grava_arquivo) {
#ifdef DEBUG
        printf("gravando filme '%s'...\n", filme->nome);
#endif
        fseek(cadastro->arquivo_filmes, 0, SEEK_END);
        fwrite(filme, 1, sizeof(filme_t), cadastro->arquivo_filmes);
    }
}

void
registra_locacao_filme(cadastro_t *cadastro,
                       elemento_filme_t *elemento_filme,
                       char disponivel)
{
    int size;
    char old_disponivel;
    char entrada[MAX_ENTRY];

    old_disponivel = elemento_filme->filme->disponivel;
    elemento_filme->filme->disponivel = disponivel;
    fseek(cadastro->arquivo_filmes,
        elemento_filme->id * sizeof(filme_t),
        SEEK_SET);
    size = fwrite(elemento_filme->filme, 1,
        sizeof(filme_t),
        cadastro->arquivo_filmes);
    if (size < sizeof(filme_t)) {
        elemento_filme->filme->disponivel = old_disponivel;
        printf("Erro no registro da locacao! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }
    fseek(cadastro->arquivo_filmes, 0, SEEK_END);
}

elemento_filme_t *
pesquisa_filme(cadastro_t *cadastro, const char *nome)
{
    elemento_filme_t *pesquisa;

    pesquisa = cadastro->filmes;

    if (!pesquisa) return NULL;
#ifdef DEBUG
    printf("pesquisando...\n");
#endif
    while (pesquisa) {
#ifdef DEBUG
        printf("   %s\n", pesquisa->filme->nome);
#endif
        if (!strncmp(pesquisa->filme->nome, nome, 50)) {
            return pesquisa;
        }
        pesquisa = pesquisa->proximo;
    }
    return NULL;
}


/* Cliente */
void
cadastra_cliente(cadastro_t *cadastro)
{
    cliente_t *cliente;
    long id = 0;
    char entrada[MAX_ENTRY];

    if (!(cliente = (cliente_t *) malloc(sizeof(cliente_t)))) {
        return;
    }

    clrscr();
    printf("Cadastro cliente\n");
    printf("==============\n\n");

    memset(entrada, 0, MAX_ENTRY);
    printf("Nome:     "); fgets(entrada, MAX_ENTRY, stdin);
    remove_linebreak(entrada);
    strncpy(cliente->nome, entrada, 50);

    if (pesquisa_cliente(cadastro, cliente->nome)) {
        printf("Cliente ja cadastrado! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }

    memset(entrada, 0, MAX_ENTRY);
    printf("Endereco: "); fgets(entrada, MAX_ENTRY, stdin);
    remove_linebreak(entrada);
    strncpy(cliente->endereco, entrada, 50);

    memset(entrada, 0, MAX_ENTRY);
    printf("Telefone: "); fgets(entrada, MAX_ENTRY, stdin);
    remove_linebreak(entrada);
    strncpy(cliente->telefone, entrada, 4);

    cliente->alugados = 0;

    inclui_cliente(cadastro, cliente, 1);
}

elemento_cliente_t *
consulta_cliente(cadastro_t *cadastro)
{
    elemento_cliente_t *elemento_cliente;
    long id = 0;
    char entrada[MAX_ENTRY];

    memset(entrada, 0, MAX_ENTRY);
    printf("Nome:     "); fgets(entrada, MAX_ENTRY, stdin);
    remove_linebreak(entrada);
    if (! (elemento_cliente = pesquisa_cliente(cadastro, entrada))) {
        printf("Cliente nao encontrado! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return NULL;
    }

    printf("Endereco: %s\n", elemento_cliente->cliente->endereco);
    printf("Telefone: %s\n", elemento_cliente->cliente->telefone);
    printf("Alugados: %d\n", elemento_cliente->cliente->alugados);
    return elemento_cliente;
}

void
inclui_cliente(cadastro_t *cadastro, cliente_t *cliente, int grava_arquivo)
{
    elemento_cliente_t *elemento_cliente;

    elemento_cliente = (elemento_cliente_t *)malloc(sizeof(elemento_cliente_t));

    if (cadastro->ultimo_cliente) {
        elemento_cliente->id = cadastro->ultimo_cliente->id + 1;
        cadastro->ultimo_cliente->proximo = elemento_cliente;
    } else {
        elemento_cliente->id = 1;
    }

    elemento_cliente->cliente = cliente;
    elemento_cliente->proximo = NULL;

    if (!cadastro->clientes) cadastro->clientes = elemento_cliente;
    cadastro->ultimo_cliente = elemento_cliente;

#ifdef DEBUG
    printf("incluido cliente '%s'\n", elemento_cliente->cliente->nome);
#endif

    if (grava_arquivo) {
#ifdef DEBUG
        printf("gravando cliente '%s'...\n", cliente->nome);
#endif
        fwrite(cliente, 1, sizeof(cliente_t), cadastro->arquivo_clientes);
    }
}

void
registra_locacao_cliente(cadastro_t *cadastro,
                         elemento_cliente_t *elemento_cliente, char locacoes)
{
    int size;
    char old_alugados;
    char entrada[MAX_ENTRY];

    old_alugados = elemento_cliente->cliente->alugados;
    elemento_cliente->cliente->alugados += locacoes;
    fseek(cadastro->arquivo_clientes, elemento_cliente->id * sizeof(cliente_t), SEEK_SET);
    size = fwrite(elemento_cliente->cliente, 1,
        sizeof(cliente_t),
        cadastro->arquivo_clientes);
    if (size < sizeof(cliente_t)) {
        elemento_cliente->cliente->alugados = old_alugados;
        printf("Erro no registro da locacao! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }
    fseek(cadastro->arquivo_clientes, 0, SEEK_END);
}

elemento_cliente_t *
pesquisa_cliente(cadastro_t *cadastro, const char *nome)
{
    elemento_cliente_t *pesquisa;

    pesquisa = cadastro->clientes;

    if (!pesquisa) return NULL;

#ifdef DEBUG
    printf("pesquisando...\n");
#endif
    while (pesquisa) {
#ifdef DEBUG
        printf("   %s\n", pesquisa->cliente->nome);
#endif
        if (!strncmp(pesquisa->cliente->nome, nome, 50)) {
            return pesquisa;
        }
        pesquisa = pesquisa->proximo;
    }
    return NULL;
}

void
loca_filme(cadastro_t *cadastro)
{
    elemento_filme_t *elemento_filme;
    elemento_cliente_t *elemento_cliente;
    char entrada[MAX_ENTRY];

    clrscr();
    printf("Locacao de filme\n");
    printf("================\n\n");

    printf("Filme\n");
    elemento_filme = consulta_filme(cadastro);

    if (!elemento_filme) {
        return;
    }

    if (!elemento_filme->filme->disponivel) {
        printf("Filme indisponivel! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }

    printf("\n\nCliente\n");
    elemento_cliente = consulta_cliente(cadastro);

    if (!elemento_cliente) {
        return;
    }

    printf("Confirma locacao? (S/n) ");
    fgets(entrada, MAX_ENTRY, stdin);
    if (entrada[0] == 'n' || entrada[0] == 'N') {
        printf("Cancelada! Tecle Enter para continuar...");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }

    registra_locacao_filme(cadastro, elemento_filme, 0);
    registra_locacao_cliente(cadastro, elemento_cliente, 1);
}

void
devolve_filme(cadastro_t *cadastro) {
    elemento_filme_t *elemento_filme;
    elemento_cliente_t *elemento_cliente;
    char entrada[MAX_ENTRY];

    clrscr();
    printf("Devolucao de filme\n");
    printf("==================\n\n");

    printf("Filme\n");
    elemento_filme = consulta_filme(cadastro);

    if (!elemento_filme) {
        return;
    }

    if (elemento_filme->filme->disponivel) {
        printf("Filme nao esta locado! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }

    printf("\n\nCliente\n");
    elemento_cliente = consulta_cliente(cadastro);

    if (!elemento_cliente) {
        return;
    }

    if (!elemento_cliente->cliente->alugados) {
        printf("Cliente nao tem locacao! Tecle Enter para continuar...\n");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }

    printf("Confirma devolucao? (S/n) ");
    fgets(entrada, MAX_ENTRY, stdin);
    if (entrada[0] == 'n' || entrada[0] == 'N') {
        printf("Cancelada! Tecle Enter para continuar...");
        fgets(entrada, MAX_ENTRY, stdin);
        return;
    }

    registra_locacao_filme(cadastro, elemento_filme, 1);
    registra_locacao_cliente(cadastro, elemento_cliente, -1);
}

cadastro_t *
carrega_cadastro()
{
    cadastro_t *cadastro;
    filme_t *filme;
    cliente_t *cliente;
    FILE *fd;
    int read;

    cadastro = (cadastro_t *)malloc(sizeof(cadastro_t));
    if (!cadastro) {
        return NULL;
    }

    cadastro->filmes = NULL;
    cadastro->clientes = NULL;
    cadastro->ultimo_filme = NULL;
    cadastro->ultimo_cliente = NULL;

    cadastro->arquivo_filmes = fopen("filmes.dat", "r+b");
    if (cadastro->arquivo_filmes) {
        for (;;) {
            filme = (filme_t *)malloc(sizeof(filme_t));
            read = fread(filme, 1, sizeof(filme_t), cadastro->arquivo_filmes);
            if (read == sizeof(filme_t)) {
                inclui_filme(cadastro, filme, 0);
            } else {
                free(filme);
                break;
            }
        }
    } else {
        cadastro->arquivo_filmes = fopen("filmes.dat", "w");
        freopen("filmes.dat", "r+b", cadastro->arquivo_filmes);
    }
    fseek(cadastro->arquivo_filmes, 0, SEEK_END);

    cadastro->arquivo_clientes = fopen("clientes.dat", "r+b");
    if (cadastro->arquivo_clientes) {
        for (;;) {
            cliente = (cliente_t *)malloc(sizeof(cliente_t));
            read = fread(cliente, 1,
                    sizeof(cliente_t),
                    cadastro->arquivo_clientes);
            if (read == sizeof(cliente_t)) {
                inclui_cliente(cadastro, cliente, 0);
            } else {
                free(cliente);
                break;
            }
        }
    } else {
        cadastro->arquivo_clientes = fopen("clientes.dat", "w");
        freopen("clientes.dat", "r+b", cadastro->arquivo_clientes);
    }
    fseek(cadastro->arquivo_clientes, 0, SEEK_END);


    return cadastro;
}


void
finalize(cadastro_t *cadastro)
{
    elemento_filme_t *temp_filme, *elemento_filme = cadastro->filmes;
    elemento_cliente_t *temp_cliente, *elemento_cliente = cadastro->clientes;

    while (elemento_filme) {
        free(elemento_filme->filme);
        temp_filme = elemento_filme;
        elemento_filme = elemento_filme->proximo;
        free(temp_filme);
    }

    while (elemento_cliente) {
        free(elemento_cliente->cliente);
        temp_cliente = elemento_cliente;
        elemento_cliente = elemento_cliente->proximo;
        free(temp_cliente);
    }

    fclose(cadastro->arquivo_filmes);
    fclose(cadastro->arquivo_clientes);

    free(cadastro);
}


int main(int argc, char *argv[])
{
    cadastro_t *cadastro;
    int i;
    char opc[MAX_MENU_ENTRY];

    char *menu_principal[6] = {
        "Cadastrar filme",
        "Cadastrar cliente",
        "Consultar filme",
        "Locar filme",
        "Devolver filme",
        "Encerrar"
    };

    cadastro = carrega_cadastro();
    if (!cadastro) {
        printf("Erro alocando memoria para cadastro!\n");
        return 1;
    }

    while (opc[0] != '6') {
        clrscr();
        printf("Menu Principal\n");
        printf("==============\n\n");
        for (i = 1; i <= 6; i++) {
            printf("   %d. %s\n", i, menu_principal[i-1]);
        }
        printf("Escolha uma opcao: ");
        fgets(opc, MAX_MENU_ENTRY, stdin);

        switch (opc[0]) {
            case '1':
                cadastra_filme(cadastro);
                break;
            case '2':
                cadastra_cliente(cadastro);
                break;
            case '3':
                clrscr();
                printf("Consulta filme\n");
                printf("==============\n\n");
                if (consulta_filme(cadastro)) {
                    printf("\nTecle Enter para continuar...\n");
                    fgets(opc, MAX_MENU_ENTRY, stdin);
                }
                break;
            case '4':
                loca_filme(cadastro);
                break;
            case '5':
                devolve_filme(cadastro);
                break;
        }
    }

    finalize(cadastro);
    return 0;
}

