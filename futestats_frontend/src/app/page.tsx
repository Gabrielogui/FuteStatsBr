import CompeticaoCard from "@/components/competicoes/CompeticaoCard";
import GraficoResumidoRanking from "@/components/rankings/GraficoResumidoRanking";
import TabelaResumidaRanking from "@/components/rankings/TabelaResumidaRanking";
import { BarChart3, Trophy } from "lucide-react";

export default function Home() {

    return (
        <div className="">
            {/* |=======| SEÇÃO PRINCIPAL (FRASE INICIAL + TEXTO + BOTÕES) |=======| */}
            <section className="bg-primary -my-14 -mx-10 py-14 px-10 flex flex-col">
                <div className="flex flex-col text-6xl font-black leading-tight mb-6 animate-in fade-in slide-in-from-left-4 duration-700">
                    <h1 className="text-white">Estatísticas do Futebol</h1>
                    <span className="text-purple-400 -mt-4">Brasileiro</span>
                </div>
                <p className="text-xl text-purple-100/70 max-w-2xl mb-10">
                    A plataforma completa para estatísticas, histórico e rankings do futebol nacional!
                </p>
            </section>

            {/* |=======| SEÇÃO DE TIMES DESTAQUES (SÉRIE A) |=======| */}
            <div className="flex flex-col md:flex-row items-center bg-white border-b border-gray-200 py-4 px-8 rounded-md shadow-lg -mt-10 ">
                <div className="flex justify-center text-center  md:items-center md:mr-6 min-w-max  
                                md:border-r border-gray-400 pr-6">
                    <span className="text-xs font-black text-primary uppercase tracking-widest">Série A <br/> 2026</span>
                </div>
                <div className="flex flex-wrap justify-between w-full overflow-hidden">
                    {Array.from({ length: 20 }).map((_, index) => (
                        <div key={index} className="h-16 w-16 rounded-full bg-gray-200 animate-pulse"></div>
                    ))}
                </div>
            </div>

            <div className="mt-8 flex flex-col gap-8">
                
                {/* |=======| PRINCIPAIS RANKINGS E GRÁFICOS |=======| */}
                <div className="flex flex-col gap-3 ">
                    <div className="flex gap-2 items-center text-primary">
                        <BarChart3 />
                        <h4 className="uppercase text-3xl font-bold">Principais Rankings</h4>
                    </div>

                    <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
                        <div className="flex flex-col gap-5">
                            <div className="flex justify-start gap-2 border-b pb-2">
                                <div className="bg-primary w-2 rounded-lg"></div>
                                <h1 className="text-2xl font-semibold ">Total de Gols nos Pontos Corridos</h1>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                <div>
                                    <TabelaResumidaRanking />
                                </div>
                                <div className="w-full">
                                    <GraficoResumidoRanking />
                                </div>
                            </div>
                        </div>

                        <div className="flex flex-col gap-5">
                            <div className="flex justify-start gap-2 border-b pb-2">
                                <div className="bg-primary w-2 rounded-lg"></div>
                                <h1 className="text-2xl font-semibold ">Total de Pontos do Brasileirão</h1>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                <div>
                                    <TabelaResumidaRanking />
                                </div>
                                <div className="w-full">
                                    <GraficoResumidoRanking />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                {/* |=======| PRINCIPAIS COMPETIÇÕES |=======| */}
                <div className="flex flex-col gap-3 ">
                    <div className="flex gap-2 items-center text-primary">
                        <Trophy />
                        <h4 className=" uppercase text-3xl font-bold">Principais Competições</h4>
                    </div>

                    <div className="flex gap-2 overflow-x-auto">
                        {Array.from({ length: 8 }).map((_, index) => ( 
                            <div key={index}>
                                <CompeticaoCard />
                            </div>
                        ))}
                    </div>

                </div>
            </div>
        </div>
    );
}
