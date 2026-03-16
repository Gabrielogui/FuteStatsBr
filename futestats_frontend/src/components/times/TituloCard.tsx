import { Badge } from "../ui/badge"

interface Title {
    id: string,
    label: string,
    count: number,
    color: string,
    list: Array<{ name: string, years: Array<number> }>
}

interface TituloCardProps {
    title: Title
}

export default function TituloCard ( { title } : TituloCardProps ) {
    return(
        <div className="flex flex-col items-center gap-3 p-6 border border-primary/20 rounded-lg bg-white shadow-md">
            <Badge className={`uppercase text-md font-semibold ${title.color}`} >{title.label}</Badge>

            <span className="text-6xl font-bold">{title.count}</span>
            <div className="flex flex-col items-center">
                {title.list.map((item) => (
                    <span key={item.name} className="text-primary font-semibold">{item.name}</span>
                ))}
            </div>
        </div>
    )
}