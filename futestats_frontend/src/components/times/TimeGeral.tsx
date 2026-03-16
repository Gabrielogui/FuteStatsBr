"use client";

import { ExternalLink, House, Info, Trophy } from "lucide-react";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "../ui/chart";
import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, XAxis, YAxis } from "recharts";
import { Button } from "../ui/button";

export default function TimeGeral () {

    const [cssVariables, setCssVariables] = useState({
            primary: '#4b2e83', 
            purple: '#a78bfa',
            gray: '#64748b',
            border: '#f1f5f9'
        });
    
        useEffect(() => {
            const root = document.documentElement;
            const style = getComputedStyle(root);
            
            setCssVariables({
                primary: style.getPropertyValue('--primary').trim() || '#4b2e83',
                purple: '#a78bfa',
                gray: style.getPropertyValue('--muted-foreground').trim() || '#64748b',
                border: style.getPropertyValue('--border').trim() || '#f1f5f9'
            });
        }, []);

    const PARTICIPACOES_DATA_MOCK = [
        { name: "Brasileirão", participacoes: 41 },
        { name: "Copa do Brasil", participacoes: 40 },
        { name: "Copa Libertadores", participacoes: 0 },
        { name: "Copa Sulamericana", participacoes: 6 },
    ]

    const chartConfig = {
        valor: {
            label: "Participações",
            color: cssVariables.purple,
        },
    };

    return(
        <div className="grid grid-cols-1 md:grid-cols-[20%_2%_78%] mt-8">
            <div className="flex flex-col gap-5">
                {/* |=======| INFORMAÇÕES GERAIS DO TIME |=======| */}
                <div className="flex flex-col gap-3 p-6 border border-primary/20 rounded-lg bg-white shadow-md">
                    <div className="flex items-center gap-2">
                        <Info size={26} />
                        <h2 className="text-xl font-bold">Informações Gerais</h2>
                    </div>
                    <div className="flex flex-col gap-2">
                        <div className="flex justify-between text-lg border-b py-2">
                            <span className="text-gray-500">Fundação</span>
                            <span className="font-semibold">1899</span>
                        </div>
                        <div className="flex justify-between text-lg border-b py-2">
                            <span className="text-gray-500">Alcunha</span>
                            <span className="font-semibold">Leão da Barra</span>
                        </div>
                        <div className="flex justify-between text-lg border-b py-2">
                            <span className="text-gray-500">Cores</span>
                            <span className="font-semibold">Rubro-negro</span>
                        </div>
                        <div className="flex justify-between text-lg border-b py-2">
                            <span className="text-gray-500">Cidade</span>
                            <span className="font-semibold">Salvador</span>
                        </div>
                        <div className="flex justify-between text-lg border-b py-2">
                            <span className="text-gray-500">Estado</span>
                            <span className="font-semibold">Bahia</span>
                        </div>
                    </div>
                </div>

                {/* |=======| ESTÁDIO DO TIME |=======| */}
                <div className="flex flex-col gap-3 p-6 border border-primary/20 rounded-lg bg-white shadow-md">
                    <div className="flex justify-between">
                        <div className="flex items-center gap-2">
                            <House size={22} />
                            <h2 className="text-xl font-bold">Estádio</h2>
                        </div>
                        <Button variant={"ghost"} size={"icon"}>
                            <ExternalLink />
                        </Button>
                    </div>
                    <div className="flex flex-col gap-2">
                        <div className="flex justify-between text-lg border-b py-2">
                            <span className="text-gray-500">Nome</span>
                            <span className="font-semibold">Barradão</span>
                        </div>
                        <div className="flex justify-between text-lg border-b py-2">
                            <span className="text-gray-500">Capacidade</span>
                            <span className="font-semibold">35000</span>
                        </div>
                        <div className="flex justify-between text-lg border-b py-2">
                            <span className="text-gray-500">Cidade</span>
                            <span className="font-semibold">Salvador</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* |=======| DIVISÃO NO MEIO DA DIV |=======| */}
            <div></div>

            <div className="flex flex-col gap-5">
                {/* |=======| HISTÓRIA DO TIME RESUMIDA |=======| */}
                <div className="flex flex-col gap-3 p-6 border border-primary/20 rounded-lg bg-white shadow-md">
                    <h2 className="text-2xl font-bold">História e Trajetória</h2>
                    <p className="pt-3 border-t text-lg text-gray-500 text-justify">
                        O Esporte Clube Vitória (conhecido como Vitória e cujo acrônimo é ECV) é um clube multiesportivo brasileiro, 
                        sediado na cidade de Salvador, no estado da Bahia. Foi fundado em 13 de maio de 1899 com o nome de Club 
                        de Cricket Victoria, mudado para Sport Club Victoria, em 1902, e, finalmente, para o atual nome em 1946. 
                        Sendo um dos clubes mais antigos do Brasil, suas cores são o vermelho e o preto, e seu mascote é o Leão.
                    </p>
                </div>

                {/* |=======| MELHORES CAMPANHAS DO TIME |=======| */}
                <div className="grid grid-cols-2 gap-5">
                    <div className="flex flex-col gap-3 p-6 border border-primary/20 rounded-lg bg-white shadow-md">
                        <div className="flex items-center gap-2">
                            <Trophy size={22} />
                            <h2 className="text-2xl font-bold">Melhores Campanhas</h2>
                        </div>
                        <div className="flex flex-col gap-2">
                            <div className="flex justify-between text-lg items-center p-5 border rounded-lg bg-primary/10">
                                <div className="flex flex-col items-start">
                                    <span className="font-semibold">Campeonato Brasileiro</span>
                                    <span className="text-sm">Vice-campeão</span>
                                </div>
                                <div>
                                    <span className="font-semibold">1993</span>
                                </div>
                            </div>
                            <div className="flex justify-between text-lg items-center p-5 border rounded-lg bg-primary/10">
                                <div className="flex flex-col items-start">
                                    <span className="font-semibold">Copa do Brasil</span>
                                    <span className="text-sm">Vice-campeão</span>
                                </div>
                                <div>
                                    <span className="font-semibold">2010</span>
                                </div>
                            </div>
                            <div className="flex justify-between text-lg items-center p-5 border rounded-lg bg-primary/10">
                                <div className="flex flex-col items-start">
                                    <span className="font-semibold">Série B</span>
                                    <span className="text-sm">Campeão</span>
                                </div>
                                <div>
                                    <span className="font-semibold">2023</span>
                                </div>
                            </div>
                            
                        </div>
                    </div>
                    <div className="flex flex-col gap-3 p-6 border border-primary/20 rounded-lg bg-white shadow-md">
                        <div className="flex items-center gap-2">
                            <Trophy size={26} />
                            <h2 className="text-2xl font-bold">Mais Participações</h2>
                        </div>

                        <ChartContainer config={chartConfig}>
                            <BarChart data={PARTICIPACOES_DATA_MOCK} layout="horizontal" margin={{ left: 20 }}>
                                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke={cssVariables.border} />
                                <YAxis type="number" hide />
                                <XAxis 
                                    type="category" 
                                    dataKey="name" 
                                    axisLine={false} 
                                    tickLine={false} 
                                    tick={{ fontSize: 13, fontWeight: 900, fill: cssVariables.gray }} 
                                    width={100}
                                />
                                <ChartTooltip
                                    cursor={{ fill: cssVariables.gray, radius: 10 }}
                                    content={<ChartTooltipContent />}
                                />
                                <Bar dataKey="participacoes" radius={[12, 12, 0, 0]} barSize={40}>
                                    {PARTICIPACOES_DATA_MOCK.map((entry, index) => (
                                        <Cell 
                                            key={index} 
                                            fill={index === 0 ? `${cssVariables.primary}` : `${chartConfig.valor.color}`} 
                                            fillOpacity={1 - (index * 0.15)}
                                        />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ChartContainer>

                    </div>
                </div>
            </div>
        </div>
    )
}