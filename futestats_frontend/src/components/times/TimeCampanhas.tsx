import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../ui/table";

export default function TimeCampanhas () {
    return (
        <div className="flex flex-col gap-8 my-8">
            <h2 className="text-2xl font-bold">Todas as Campanhas</h2>

            <div>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Ano</TableHead>
                            <TableHead>J</TableHead>
                            <TableHead>Comp</TableHead>
                            <TableHead>Clas</TableHead>
                            <TableHead>P</TableHead>
                            <TableHead>V</TableHead>
                            <TableHead>E</TableHead>
                            <TableHead>D</TableHead>
                            <TableHead>GM</TableHead>
                            <TableHead>GS</TableHead>
                            <TableHead>Apr</TableHead>
                        </TableRow>
                    </TableHeader>

                    <TableBody>
                        <TableRow>
                            <TableCell>2026</TableCell>
                            <TableCell>20</TableCell>
                            <TableCell>Campeonato Brasileiro</TableCell>
                            <TableCell>7º</TableCell>
                            <TableCell>58</TableCell>
                            <TableCell>17</TableCell>
                            <TableCell>07</TableCell>
                            <TableCell>14</TableCell>
                            <TableCell>63</TableCell>
                            <TableCell>49</TableCell>
                            <TableCell>XX%</TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>

        </div>
    )
}