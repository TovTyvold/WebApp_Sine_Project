import { useCallback } from "react";
import { Handle, Position } from "reactflow";
import NumberInput from "./NumberInput";
import SliderInput from "./SliderInput";

function PanNode({ data, id }: any) {
  const onChangePercent = useCallback(
    (event: any) => {
      data.percent = event.target.value;
    },
    [data]
  );

  return (
    <div className="pan-node">
      <b>Pan</b>
      {/* <Handle type='source' position={Position.Right} /> */}
      <Handle id={"out-" + id} type="source" position={Position.Right} />
      <Handle
        id={"percent-" + id}
        type="target"
        position={Position.Left}
        style={{ top: 50 }}
      />
      <Handle
        id={"points-" + id}
        type="target"
        position={Position.Left}
        style={{ top: 110 }}
      />
      <hr />
      <SliderInput
        name="percent"
        defaultValue={50}
        min={0}
        max={100}
        unit="%"
        onChange={onChangePercent}
      />
      <br></br>
      Points

    </div>
  );
}

export default PanNode;
