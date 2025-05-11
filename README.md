# SistemaDeMusicaPersistencia

Neste trabalho será desenvolvido um CRUD para um sistema de musica, as entidades principais desse sistema são:
- Artista
<table>
  <thead>
    <tr>
      <th>Campo</th>
      <th>Tipo de dado</th>
      <th>Restrições</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>Inteiro</td>
      <td>Chave primária, não nulo, auto incremento</td>
      <td>Identificador único do artista</td>
    </tr>
    <tr>
      <td>nome</td>
      <td>Texto (string)</td>
      <td>Não nulo, único</td>
      <td>Nome do artista</td>
    </tr>
    <tr>
      <td>gênero</td>
      <td>Texto (string)</td>
      <td>Não nulo</td>
      <td>Gênero musical predominante</td>
    </tr>
    <tr>
      <td>data_estreia</td>
      <td>Data</td>
      <td>Não nulo</td>
      <td>Data de estreia na carreira</td>
    </tr>
    <tr>
      <td>sobre</td>
      <td>Texto longo</td>
      <td>Opcional</td>
      <td>Informações biográficas ou curiosidades sobre o artista</td>
    </tr>
  </tbody>
</table>

- Album
<table>
  <thead>
    <tr>
      <th>Campo</th>
      <th>Tipo de dado</th>
      <th>Restrições</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>Inteiro</td>
      <td>Chave primária, não nulo, auto incremento</td>
      <td>Identificador único do álbum</td>
    </tr>
    <tr>
      <td>nome</td>
      <td>Texto (string)</td>
      <td>Não nulo</td>
      <td>Nome do álbum</td>
    </tr>
    <tr>
      <td>id_artista</td>
      <td>Inteiro</td>
      <td>Chave estrangeira, não nulo</td>
      <td>ID do artista relacionado (referencia <code>artista.id</code>)</td>
    </tr>
    <tr>
      <td>data_lancamento</td>
      <td>Data</td>
      <td>Não nulo</td>
      <td>Data oficial de lançamento do álbum</td>
    </tr>
    <tr>
      <td>gravadora</td>
      <td>Texto (string)</td>
      <td>Não nulo</td>
      <td>Nome da gravadora ou selo responsável pelo álbum</td>
    </tr>
  </tbody>
</table>

- Musica
<table>
  <thead>
    <tr>
      <th>Campo</th>
      <th>Tipo de dado</th>
      <th>Restrições</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>Inteiro</td>
      <td>Chave primária, não nulo, auto incremento</td>
      <td>Identificador único da música</td>
    </tr>
    <tr>
      <td>nome</td>
      <td>Texto (string)</td>
      <td>Não nulo</td>
      <td>Nome ou título da música</td>
    </tr>
    <tr>
      <td>data_lancamento</td>
      <td>Data</td>
      <td>Não nulo</td>
      <td>Data oficial de lançamento da música</td>
    </tr>
    <tr>
      <td>id_album</td>
      <td>Inteiro</td>
      <td>Chave estrangeira, não nulo</td>
      <td>ID do álbum ao qual a música pertence (referencia <code>album.id</code>)</td>
    </tr>
    <tr>
      <td>duracao</td>
      <td>Inteiro</td>
      <td>Não nulo</td>
      <td>Duração total da música em segundos</td>
    </tr>
  </tbody>
</table>

## Atribuições
<table>
  <tr>
     <td align="center"><a href="https://github.com/JoseVitorNobreUFC"><img src="https://avatars.githubusercontent.com/u/62249331?v=4" width="100px;" alt="José Vitor"/><br /><sub><b>José Vitor</b></sub></a><br /><a href="https://github.com/JoseVitorNobreUFC" title="BackEnd">
     </a><br/>
     <span>CRUD Artista, Album, tasks f2, f3, f5, f7 e documentação</span>
     </td>
     <td align="center"><a href="https://github.com/alexsonalmeida"><img src="https://avatars.githubusercontent.com/u/101877352?v=4" width="100px;" alt="Higor Santiago"/><br /><sub><b>Alexson Almeida</b></sub></a><br /><a href="https://github.com/alexsonalmeida" title="FrontEnd">
     </a><br/>
     <span>CRUD Musicas, tasks f2, f4, f6, f8 e testes</span>
     </td>
  </tr>
</table>
