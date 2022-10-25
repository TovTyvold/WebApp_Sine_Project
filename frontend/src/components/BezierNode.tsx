import { useCallback, useRef } from 'react';
import { BezierCurveEditor } from 'react-bezier-curve-editor';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function BezierNode({ data, id }: any) {
  const point = useRef<[number,number,number,number]>([0.5,0.5,1,1])

  const bezierOnChange = useCallback((points: Array<number>) => {
    points[2] = 1
    points[3] = 1

    point.current[0] = points[0]
    point.current[1] = points[1]

    data.x = point.current[0]
    data.y = point.current[1]
  }, [point])

  return (
    <div className='bezier-node'>
        <b>Bezier</b>
        {/* <Handle type='source' position={Position.Right} /> */}
        <Handle id={'out-' + id} type='source' position={Position.Right} />
        {/* <NumberInput label="Lable" name="value" onChange={onChange}/> */}
        <div className="nodrag">
            <BezierCurveEditor 
                size={200} 
                outerAreaSize={0} 
                fixedHandleColor={"#1cdb42"} 
                endHandleColor={"#1cdb42"} 
                endHandleClassName="nostroke" 
                endHandleActiveClassName="nodrag" 
                handleLineColor={"#ffffff"} 
                value={point.current}
                onChange={bezierOnChange}
                rowColor={"#ffffff"}/>
        </div>
    </div>
  );
}

export default BezierNode;
