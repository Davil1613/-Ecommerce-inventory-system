export interface IProductStock {
  ID_Produto: number;
  NomeProduto: string;
  ValorUnitario: number;
  Quantidade: number;
  ValorTotal: number;
  DataUltimaAtualizacao: string; // A API envia a data como string no formato 'AAAA-MM-DD'
}