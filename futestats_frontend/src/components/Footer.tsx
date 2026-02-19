import { BarChart3, Instagram, Linkedin, Mail, Phone } from "lucide-react";

export default function Footer() {
    return(
        <footer className="bg-[#0f172a] flex flex-col">
            
            <div className="bg-azul-escuro text-white grid grid-cols-2  md:flex justify-between gap-5 px-10 pt-10 pb-5 items-start w-full">
                {/* |=======| LOGO + CNPJ DA EMPRESA |=======| */}
                <div className="flex flex-col flex-1/4 gap-3">
                    <div className="flex items-center gap-2">
                        <BarChart3 />
                        <h1 className="text-2xl font-semibold">FuteStats BR</h1>
                    </div>
                    <p className="text-sm text-gray-400">
                        Estatísticas e dados históricos do futebol brasileiro
                    </p>
                    <span className="text-gray-400">CNPJ: 00.000.000/0001-00</span>
                </div>

                <div className="flex flex-col flex-1/4 gap-3">
                    <h3 className="text-2xl font-semibold">Navegação</h3>
                    <div className="flex flex-col">
                        <span className="text-gray-400">Sobre o projeto</span>
                        <span className="text-gray-400">Times</span>
                        <span className="text-gray-400">Ranings</span>
                    </div>
                </div>

                {/* |=======| CONTATO |=======| */}
                <div className="flex flex-col flex-1/4 gap-3">
                    <h3 className="text-2xl font-semibold">Contato</h3>
                    <div className="flex flex-col md:flex-row gap-2 text-gray-400">
                        <Mail />
                        <span className="">futestats@example.com</span>
                    </div>
                    <div className="flex flex-col md:flex-row gap-2 text-gray-400">
                        <Phone />
                        <span className="">(71) 9 0000-0000</span>
                    </div>
                </div>

                {/* |=======| REDES SOCIAIS |=======| */}
                <div className="flex flex-col flex-1/4 gap-3">
                    <h3 className="text-2xl font-semibold">Redes Sociais</h3>
                    <div className="flex flex-row gap-4 text-gray-400">
                        <div className="hover:scale-105 hover:text-white transition-all cursor-pointer">
                            <Instagram />
                        </div>
                        <div className="hover:scale-105 hover:text-white transition-all cursor-pointer">
                            <Linkedin />
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-[#1e293b] flex items-center w-full px-2 py-2 justify-center">
                <span className="text-white">© 2025 FuteStats BR. Todos os direitos reservados.</span>
            </div>

        </footer>
    )
}