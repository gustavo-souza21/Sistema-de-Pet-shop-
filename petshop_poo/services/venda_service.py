from models.venda import Venda
from models.excecoes import ProdutoNaoEncontradoError, VendaNaoEncontradaError
from repositories.venda_repository import VendaRepository
from repositories.produto_repository import ProdutoRepository


class VendaService:
    def __init__(self, repositorio: VendaRepository = None, produto_repositorio: ProdutoRepository = None):
        self.repositorio = repositorio or VendaRepository()
        self.produto_repositorio = produto_repositorio or ProdutoRepository()

    def abrir_venda(self, id_cliente=None, id_agendamento=None) -> Venda:
        venda = Venda(id_cliente=id_cliente, id_agendamento=id_agendamento)
        return self.repositorio.criar(venda)

    def adicionar_servico(self, id_venda, id_agendamento, valor_unitario, quantidade=1):
        return self.repositorio.adicionar_item_servico(id_venda, id_agendamento, valor_unitario, quantidade)

    def adicionar_produto(self, id_venda, id_produto, quantidade=1):
        """
        Registra a venda de um produto E da baixa no estoque, tratando as
        duas operacoes como uma coisa so: se o estoque nao for suficiente,
        nada e gravado no banco.
        """
        produto = self.produto_repositorio.buscar_por_id(id_produto)
        if produto is None:
            raise ProdutoNaoEncontradoError(id_produto)

        produto.baixar_estoque(quantidade)  # levanta EstoqueInsuficienteError se necessario

        item = self.repositorio.adicionar_item_produto(id_venda, id_produto, produto.preco, quantidade)
        self.produto_repositorio.atualizar(id_produto, estoque=produto.estoque)
        return item

    def detalhar(self, id_venda) -> Venda:
        venda = self.repositorio.detalhar(id_venda)
        if venda is None:
            raise VendaNaoEncontradaError(id_venda)
        return venda

    def listar_todas(self):
        return self.repositorio.listar()

    def remover(self, id_venda) -> bool:
        removida = self.repositorio.deletar(id_venda)
        if not removida:
            raise VendaNaoEncontradaError(id_venda)
        return True
