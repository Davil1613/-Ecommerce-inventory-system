import Link from 'next/link';

export default function Navbar() {
    return(
        <nav className="bg-gray-800 text-white p-4 mb-6">
            <ul className = "flex space-x-4">
                <li><Link href="/">Início</Link></li>
                <li><Link href="/estoque">Estoque</Link></li>
                <li><Link href="/add_product">Adicionar Produtos</Link></li>
                <li><Link href="/remove_product">Remover Produtos</Link></li>
            </ul>
        </nav>
    )
}