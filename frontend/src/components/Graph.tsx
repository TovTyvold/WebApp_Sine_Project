import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

const Graph = (props: any) => {
  return (
    <div>
      <LineChart
        width={1200}
        height={600}
        data={props.data}
        margin={{ top: 5, right: 20, bottom: 5, left: 20 }}>
        <Line
          type='monotone'
          dataKey='y'
          stroke='#1f939e'
          strokeWidth={4}
          legendType='none'
          dot={false}
          strokeLinecap='round'
        />
        <CartesianGrid stroke='none' strokeDasharray='5 5' />
        <XAxis hide={true} />
        <YAxis hide={true} />
        <Tooltip />
      </LineChart>
    </div>
  );
};

export default Graph;
