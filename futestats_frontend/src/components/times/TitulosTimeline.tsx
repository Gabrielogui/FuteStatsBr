import { cn } from "@/lib/utils";
import { TrophyIcon } from "lucide-react";

interface Trophy {
    id: number;
    year: number;
    competition_name: string;
    type?: 'internacional' | 'nacional' | 'regional' | 'estadual';
}

interface TeamTrophiesTimelineProps {
    trophies?: Trophy[];
    foundationYear?: number;
}

 
// DADOS MOCK
const MOCK_DATA: Trophy[] = [
    { id: 1, year: 2023, competition_name: 'Copa do Brasil', type: 'nacional' },
    { id: 2, year: 2023, competition_name: 'Supercopa do Brasil', type: 'nacional' },
    { id: 3, year: 2021, competition_name: 'Campeonato Brasileiro', type: 'nacional' },
    { id: 4, year: 2019, competition_name: 'Copa Libertadores', type: 'internacional' },
    { id: 5, year: 1992, competition_name: 'Campeonato Brasileiro', type: 'nacional' },
];

export default function TitulosTimeline({ trophies = MOCK_DATA, foundationYear = 1900 }: TeamTrophiesTimelineProps) {

    const currentYear = new Date().getFullYear();
  
    // Lista de todos os anos desde a fundação
    const allYears = Array.from(
        { length: currentYear - foundationYear + 1 },
        (_, i) => currentYear - i
    );

    const groupedTrophies = trophies.reduce((acc, trophy) => {
        if (!acc[trophy.year]) acc[trophy.year] = [];
        acc[trophy.year].push(trophy);
        return acc;
    }, {} as Record<number, Trophy[]>);


    return(
        <div className="w-full max-w-3xl mx-auto py-8 px-6">
            <div className="relative">
                {/* Linha Vertical da Timeline - Ajustada para a esquerda */}
                <div className="absolute left-15 md:left-25 top-0 bottom-0 w-px bg-linear-to-b from-primary/50 via-border to-transparent" />

                <div className="flex flex-col gap-2">
                {allYears.map((year) => {
                    const yearTrophies = groupedTrophies[year] || [];
                    const hasTrophies = yearTrophies.length > 0;

                    return (
                    <div key={year} className="group relative flex items-start min-h-10">
                        
                        {/* ANO (Esquerda) */}
                        <div className="w-12.5 md:w-20 shrink-0 pt-1 text-right pr-4">
                        <span className={cn(
                            "text-xs font-mono transition-all duration-300",
                            hasTrophies 
                            ? "text-primary text-base font-bold" 
                            : "text-muted-foreground/30 group-hover:text-muted-foreground/60"
                        )}>
                            {year}
                        </span>
                        </div>

                        {/* MARCADOR (Centro) */}
                        <div className="relative flex flex-col items-center justify-start w-5 md:w-10 pt-2 z-10">
                        {hasTrophies ? (
                            <div className="w-3 h-3 rounded-full bg-primary ring-4 ring-background shadow-[0_0_10px_rgba(var(--color-primary),0.4)] animate-in fade-in zoom-in duration-500" />
                        ) : (
                            <div className="w-1.5 h-1.5 rounded-full bg-border group-hover:bg-primary/30 transition-colors" />
                        )}
                        </div>

                        {/* CONTEÚDO / TÍTULOS (Direita) */}
                        <div className="flex-1 pb-4 pl-4">
                        {hasTrophies ? (
                            <div className="grid gap-2 animate-in slide-in-from-left-2 duration-300">
                            {yearTrophies.map((t) => (
                                <div 
                                key={t.id} 
                                className="flex items-center gap-3 p-3 rounded-xl bg-white border border-border/50 hover:border-primary/30 hover:bg-secondary/40 transition-all cursor-default"
                                >
                                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-background shadow-xs text-amber-500">
                                    <TrophyIcon size={16} />
                                </div>
                                <div>
                                    <p className="text-sm font-bold leading-tight">{t.competition_name}</p>
                                    <span className="text-[10px] uppercase font-semibold text-muted-foreground tracking-widest">
                                    {t.type || 'Oficial'}
                                    </span>
                                </div>
                                </div>
                            ))}
                            </div>
                        ) : (
                            // Placeholder sutil para anos sem título para manter o ritmo visual
                            <div className="h-4" />
                        )}
                        </div>
                    </div>
                    );
                })}
                </div>
            </div>
            </div>

    );
}