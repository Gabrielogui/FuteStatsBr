import TituloCard from "./TituloCard"

interface Titles {
    total: number,
    categories: Array<{ id: string, label: string, count: number, color: string, list: Array<{ name: string, years: Array<number> }> }>
}

export default function TimeTitulos () {

    const titles : Titles = {
        total: 35,
        categories: [
        { id: 'intl', label: 'Internacionais', count: 0, list: [], color: 'bg-amber-100 text-amber-700' },
        { id: 'nat', label: 'Nacionais', count: 1, color: 'bg-amber-100 text-amber-700', list: [
            { name: 'Campeonato Brasileiro - Série B', years: [2023] }
        ]},
        { id: 'reg', label: 'Regionais', count: 4, color: 'bg-emerald-100 text-emerald-700', list: [
            { name: 'Copa do Nordeste', years: [1997, 1999, 2003, 2010] },
            { name: 'Torneio José Américo de Almeida Filho', years: [1976] },
        ]},
        { id: 'sta', label: 'Estaduais', count: 30, color: 'bg-primary/10 text-primary', list: [
            { name: 'Campeonato Baiano', years: [1908, 1909, 1953, 1955, 1957, 1964, 1965, 1972, 1980, 1985, 1989, 1990, 1992, 1995, 1996, 1997, 1999, 2000, 2002, 2003, 2004, 2005, 2007, 2008, 2009, 2010, 2013, 2016, 2017, 2024] }
        ]},
        ]
    }


    return(
        <div className="flex flex-col mt-8">
            {/* |=======| TÍTULOS POR CATEGORIA |=======| */}
            <div className="grid grid-cols-4 gap-5">
                {titles.categories.map((category) => (
                    <TituloCard key={category.id} title={category} />
                ))}
            </div>
        </div>
    )
}