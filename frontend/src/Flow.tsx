import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  Node,
  addEdge,
  updateEdge,
  Background,
  Edge,
  Connection,
  useNodesState,
  useEdgesState,
  OnSelectionChangeParams,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './flow-node.css';

import { ContextMenu } from './components/ContextMenu';
import ControllButtons from './components/ControlButtons';
import EnvelopeNode from './components/EnvelopeNode';
import OscillatorNode from './components/OscillatorNode';
import OperationNode from './components/OperationNode';
import EffectNode from './components/EffectNode';
import OutputNode from './components/OutputNode';
import MixNode from './components/MixNode';
import ValueNode from './components/ValueNode';
import BezierNode from './components/BezierNode';

const initialNodes: Node[] = [
  {
    id: 'output0',
    type: 'out',
    data: {
      sustainTime: { sec: 2 },
      pan: { percent: 50 },
    },
    position: { x: 850, y: 250 },
    deletable: false,
  },
];

const initialEdges: Edge[] = [];

const defaultData: Map<string, Object> = new Map([
  ['oscillator', { frequency: 440, amplitude: 1, shape: 'sin' }],
  ['operation', { opType: 'sum' }],
  ['value', { value: 1 }],
  [
    'envelope',
    {
      attack: { ms: 20 },
      decay: { ms: 20 },
      sustain: { percent: 60 },
      release: { ms: 20 },
    },
  ],
  [
    'bezier',
    {
      points: [
        [0, 0],
        [0.5, 0.5],
        [1, 1],
      ],
      start: 0,
      end: 1,
    },
  ],
  ['mix', { percent: 50, value0: 0, value1: 1 }],
]);

const Flow = ({ submit }: any) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const currentNode = useRef<Node>();
  const [instance, setInstance] = useState<any>(null);
  const edgeUpdateSuccessful = useRef(true);
  const [showContextMenu, setShowContextMenu] = useState(false);
  const [contextPosition, setContextPosition] = useState({ x: 0, y: 0 });
  const [currView, setCurrView] = useState({ x: 0, y: 0, zoom: 1 });
  const idRef = useRef<any>({
    oscillator: 0,
    envelope: 0,
    operation: 0,
    effect: 0,
    value: 0,
    bezier: 0,
    mix: 0,
  });

  const nodeTypes = useMemo(
    () => ({
      oscillator: OscillatorNode,
      envelope: EnvelopeNode,
      operation: OperationNode,
      effect: EffectNode,
      value: ValueNode,
      out: OutputNode,
      bezier: BezierNode,
      mix: MixNode,
    }),
    []
  );

  const getFlow = useCallback(() => {
    if (instance) {
      const nodesList = instance.getNodes();
      const edgesList = instance.getEdges();

      submit({ nodes: nodesList, edges: edgesList });
    }
  }, [instance]);

  useEffect(() => {
    const playListener = (event: any) => {
      if (event.code === 'Space') {
        event.preventDefault();
        getFlow();
      }
    };
    document.addEventListener('keydown', playListener);
    return () => {
      document.removeEventListener('keydown', playListener);
    };
  }, [getFlow]);

  const addNode = useCallback(
    (nodeType: string, nodePos: any, view: any, data?: any) => {
      let nodeData: Object;
      if (data) {
        nodeData = data;
      } else {
        //perform a deep copy of defaultData of nodeType
        // const def = JSON.parse(JSON.stringify(defaultData.get(nodeType)));
        const def = defaultData.get(nodeType);
        nodeData = def !== undefined ? JSON.parse(JSON.stringify(def)) : {};
      }

      const x = (1 / view.zoom) * (nodePos.x - view.x);
      const y = (1 / view.zoom) * (nodePos.y - view.y);

      const newNode = {
        id: `${nodeType}${idRef.current[nodeType]++}`,
        position: { x: x, y: y },
        type: nodeType,
        data: nodeData,
      };

      setNodes((nds) => nds.concat(newNode));
      setShowContextMenu(false);
    },
    []
  );

  useEffect(() => {
    const duplicateListener = (event: any) => {
      if (event.ctrlKey && event.key === 'd') {
        event.preventDefault();
        if (currentNode.current) {
          const c: Node = currentNode.current;
          const newPos = { x: c.position.x + 100, y: c.position.y + 100 };
          if (c.type) addNode(c.type, newPos, currView, c.data);
        }
      }
    };
    document.addEventListener('keydown', duplicateListener);
    return () => {
      document.removeEventListener('keydown', duplicateListener);
    };
  }, []);

  useEffect(() => {
    const ctxMenuListener = (event: any) => {
      if (event.shiftKey && event.key === 'A') {
        event.preventDefault();
        onPaneContextMenu(event, true);
      }
    };
    document.addEventListener('keydown', ctxMenuListener);
    return () => {
      document.removeEventListener('keydown', ctxMenuListener);
    };
  }, []);

  const onSelectionChange = useCallback(
    ({ nodes, edges }: OnSelectionChangeParams) => {
      nodes.forEach((node: Node) => {
        if (node.selected) currentNode.current = node;
      });
    },
    []
  );

  const removeNode = useCallback((n: Node) => {
    setNodes((nds) => nds.filter((node) => node.id !== n.id));
  }, []);

  const onConnect = useCallback(
    (params: Edge | Connection) =>
      setEdges((edges) =>
        addEdge({ ...params, style: { color: 'red' } }, edges)
      ),
    [setEdges]
  );

  const onEdgeUpdateStart = useCallback(() => {
    edgeUpdateSuccessful.current = false;
  }, []);

  const onEdgeUpdate = useCallback(
    (oldEdge: Edge, newConnection: Connection) => {
      edgeUpdateSuccessful.current = true;
      setEdges((els) => updateEdge(oldEdge, newConnection, els));
    },
    []
  );

  const onEdgeUpdateEnd = useCallback((_: any, edge: Edge) => {
    if (!edgeUpdateSuccessful.current) {
      setEdges((eds) => eds.filter((e) => e.id !== edge.id));
    }
  }, []);

  const onPaneContextMenu = useCallback((event: any, hotkey?: boolean) => {
    event.preventDefault();
    let viewport_x;
    let viewport_y;
    const boundingBox = event.target.getBoundingClientRect();

    console.log(boundingBox);
    if (hotkey) {
      viewport_x = 300;
      viewport_y = 200;
    } else {
      viewport_x = event.pageX - boundingBox.left;
      viewport_y = event.pageY - boundingBox.top;
    }

    setContextPosition({ x: viewport_x, y: viewport_y });
    setShowContextMenu(true);
  }, []);

  const onPaneClick = useCallback((event: any) => {
    setShowContextMenu(false);
  }, []);

  const onMoveEnd = useCallback((event: any, view: any) => {
    setCurrView(view);
  }, []);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onPaneContextMenu={onPaneContextMenu}
      onPaneClick={onPaneClick}
      onSelectionChange={onSelectionChange}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onEdgeUpdate={onEdgeUpdate}
      onEdgeUpdateStart={onEdgeUpdateStart}
      onEdgeUpdateEnd={onEdgeUpdateEnd}
      onConnect={onConnect}
      nodeTypes={nodeTypes}
      onInit={setInstance}
      onMoveEnd={onMoveEnd}
      defaultViewport={currView}
      deleteKeyCode={['Backspace', 'Delete']}
      onNodesDelete={(n: any) => {
        removeNode(n);
      }}>
      <ContextMenu
        show={showContextMenu}
        position={contextPosition}
        onClick={(n: any) => addNode(n, contextPosition, currView)}
      />
      <ControllButtons getFlow={getFlow} />
      <Background />
    </ReactFlow>
  );
};

export default (props: any) => (
  <ReactFlowProvider>
    <Flow submit={props.submit} />
  </ReactFlowProvider>
);
