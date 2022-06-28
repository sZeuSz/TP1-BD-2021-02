# Objetivo

Este trabalho tem por objetivo pôr em prática a modelagem de esquemas relacionais e a criação, modificação e consulta em relações utilizando uma LMD. Os dados utilizados foram retirados do SNAP (Stanford Network Analysis Project).

## Como rodar o projeto na sua máquina

Se você está usando o github (clone o projeto para sua máquina)

```
git clone https://github.com/sZeuSz/TP1-BD-2021-02.git
```

Se você está usando o zip (extraia o arquivo para sua máquina)

## Commands (docker/docker-compose precisa estar instalado na sua máquina)

No diretório do projeto, como super usuário utilize os seguintes comandos:

Para colocar os serviços no ar

```
docker-compose up
```

Abra uma segunda aba de terminal e utilize o comando:

```
docker exec -it tp1_mateus_roseno_richard_postgres_python bash
```

Após esse comando, você pode rodar os script dentro do container ^^, vai ver algo desse tipo:

```
root@64bc0ea2b9d7:/app#
```

Para rodar o script que criar as tabelas e popula o banco de dados, utilize o comando:

```
python3 tp1_3.2.py
```

Para rodar o script do dashboard, utilize o comando:

```
python3 tp1_3.3.py
```

## Para sair, utilize CRLT + D e verá:

```
root@64bc0ea2b9d7:/app#
exit
```

### Contribuidores

[![mateus][mateus_avatar]][mateus_avatar]<br/>[Mateus][mateus_homepage]

[![richard][richard_avatar]][richard_avatar]<br/>[Richard][richard_homepage]

[![roseno][roseno_avatar]][roseno_avatar]<br/>[roseno][roseno_homepage]

[mateus_homepage]: https://github.com/Mateuxx
[mateus_avatar]: https://github.com/Mateuxx.png?size=150
[richard_avatar]: https://github.com/richardauzier-afk.png?size=151
[richard_homepage]: https://github.com/richardauzier-afk
[roseno_homepage]: https://github.com/sZeuSz
[roseno_avatar]: https://github.com/sZeuSz.png?size=150
