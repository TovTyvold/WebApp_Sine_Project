import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';


export default function Graph() {
    const data = [{x: 0, y: 0}, {x: 0.25, y: 1}, {x: 0.5, y: 0}, {x: 0.75, y: -1}, {x: 1, y: 0}]

    return (
        <div>
            <LineChart width={600} height={300} data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                <Line type="monotone" dataKey="y" stroke="#8884d8" />
                <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                <XAxis dataKey="x" />
                <YAxis />
                <Tooltip />
            </LineChart>
        </div>
    );
}