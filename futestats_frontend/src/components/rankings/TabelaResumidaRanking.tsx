import { BarChart3 } from "lucide-react";
import { Button } from "../ui/button";

export default function TabelaResumidaRanking() {
    return (
        <div className="flex flex-col gap-2 border p-3 rounded-2xl shadow-sm">
            <div className="flex flex-col justify-between gap-2">
                {Array.from({ length: 3 }).map((_, index) => (
                    <div key={index} className="flex items-center justify-between p-4 rounded-2xl bg-slate-50 border border-slate-100 group hover:border-purple-200 transition-all">
                        <div className="flex items-center gap-4">
                            <span className={`text-2xl font-black ${index === 0 ? 'text-amber-500' : index === 1 ? 'text-slate-400' : 'text-amber-700'}`}>
                                {index + 1}º
                            </span>
                            <span className="font-bold text-slate-700 text-lg">Vitória</span>
                        </div>
                        <span className="font-black text-primary bg-primary/10 px-3 py-1 rounded-lg text-sm">
                            X Gols
                        </span>
                    </div>
                ))}
            </div>
            <div className="flex w-full ">
                <Button variant={"default"} className="w-full cursor-pointer">
                    <BarChart3 />
                    Ver Tabela Completa
                </Button>
            </div>
        </div>
    )
}