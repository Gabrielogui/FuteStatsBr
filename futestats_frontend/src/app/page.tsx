
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
                <div className="flex justify-center text-center pl-6 md:items-center md:mr-6 min-w-max  
                                md:border-r border-gray-400 pr-6">
                    <span className="text-xs font-black text-primary uppercase tracking-widest">Série A <br/> 2026</span>
                </div>
                <div className="flex flex-wrap justify-between w-full overflow-hidden">
                    {Array.from({ length: 20 }).map((_, index) => (
                        <div key={index} className="h-16 w-16 rounded-full bg-gray-200 animate-pulse"></div>
                    ))}
                </div>
            </div>
        </div>
    );
}
