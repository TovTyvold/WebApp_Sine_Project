import { useCallback, useRef } from 'react';
import { BezierCurveEditor } from 'react-bezier-curve-editor';
import { Handle, Position } from 'reactflow';
import NumberInput from '../components/NumberInput';

function BezierNode({ data, id, selected }: any) {
  const point = useRef<[number, number, number, number]>([0.5, 0.5, 1, 1]);
  const start = useRef<number>(data.start);
  const end = useRef<number>(data.end);

  const bezierOnChange = useCallback(
    (points: Array<number>) => {
      points[2] = 1;
      points[3] = 1;

      point.current[0] = points[0];
      point.current[1] = points[1];

      data.points = [
        [start.current, 0],
        [
          point.current[0] + (end.current + start.current) / 2,
          point.current[1],
        ],
        [end.current, 1],
      ];
    },
    [point, data]
  );

  const onChangeStart = useCallback(
    (event: any) => {
      event.preventDefault();
      start.current = parseFloat(event.target.value);

      bezierOnChange(point.current);
    },
    [bezierOnChange]
  );

  const onChangeEnd = useCallback(
    (event: any) => {
      event.preventDefault();
      end.current = parseFloat(event.target.value);

      bezierOnChange(point.current);
    },
    [bezierOnChange]
  );

  return (
    <div className={'bezier-node' + (selected ? ' node-selected' : '')}>
      <b>Bezier</b>
      {/* <Handle type='source' position={Position.Right} /> */}
      <Handle id={'out-' + id} type='source' position={Position.Right} />
      {/* <NumberInput label="Lable" name="value" onChange={onChange}/> */}
      <div className='nodrag'>
        <BezierCurveEditor
          size={200}
          outerAreaSize={0}
          fixedHandleColor={'#1cdb42'}
          endHandleColor={'#1cdb42'}
          endHandleClassName='nostroke'
          endHandleActiveClassName='nodrag'
          handleLineColor={'#ffffff'}
          value={point.current}
          onChange={bezierOnChange}
          rowColor={'#ffffff'}
        />
      </div>
      <hr />
      <NumberInput
        defaultValue={start.current}
        label='Start'
        name='start'
        onChange={onChangeStart}
      />
      <NumberInput
        defaultValue={end.current}
        label='End'
        name='end'
        onChange={onChangeEnd}
      />
    </div>
  );
}

export default BezierNode;
