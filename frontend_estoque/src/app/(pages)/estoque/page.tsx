import { getStock } from "@/lib/api"
import { IProductStock } from "@/types"

export default async function EstoquePage() {

    const stock: IProductStock[] = await getStock();
    return (
        <div>
            <h1> Estoque Atual</h1>
            <p> Esses são seus produtos atuais: </p>
            <div>
                <table>
                    <thead>
                        <tr>
                            <th scope='col' className="py-3 px-6">ID</th>
                            <th scope='col' className="py-3 px-6">PRODUTO</th>
                            <th scope='col' className="py-3 px-6">VALOR UNIDADE</th>
                            <th scope='col' className="py-3 px-6">QUANTIDADE</th>
                            <th scope='col' className="py-3 px-6">VALOR TOTAL</th>
                            <th scope='col' className="py-3 px-6">DATA ATUALIZAÇÃO</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stock.length === 0 ?(
                        <tr>
                            <td colSpan={6}>NENHUM PRODUTO NO ESTOQUE</td>
                        </tr>
                        ): (
                        stock.map((product) => (
                            <tr key={product.ID_Produto}>
                                <th scope="row"> {product.ID_Produto}</th>
                                <td className="py-4 px-6">{product.NomeProduto}</td>
                                <td className="py-4 px-6">{product.ValorUnitario.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
                                <td className="py-4 px-6">{product.Quantidade}</td>
                                <td className="py-4 px-6">{product.ValorTotal.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})}</td>
                                <td className="py-4 px-6">{new Date(product.DataUltimaAtualizacao).toLocaleDateString('pt-BR', {timeZone: 'UTC'})}</td>
                            </tr>
                        ))
                    )}
                    </tbody>
                </table>
            </div>
        </div>
    )
};