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
  ReactFlowInstance,
  Viewport,
  XYPosition,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './Flow.css';

import { ContextMenu } from './components/ContextMenu';
import ControllButtons from './components/ControlButtons';
import EnvelopeNode from './nodes/EnvelopeNode';
import OscillatorNode from './nodes/OscillatorNode';
import OutputNode from './nodes/OutputNode';
import MixNode from './nodes/MixNode';
import ValueNode from './nodes/ValueNode';
import BezierNode from './nodes/BezierNode';
import NoiseNode from './nodes/NoiseNode';
import FilterNode from './nodes/FilterNode';
import VibratoNode from './nodes/VibratoNode';
import DiracNode from './nodes/DiracNode';
import ReverbNode from './nodes/ReverbNode';
import SumNode from './nodes/SumNode';
import MultiNode from './nodes/MultiNode';

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
  ['noise', { color: 'white', intensity: 0.8 }],
  ['filter', { filterType: 'hpf', cutoff: 500 }],
  ['vibrato', { speed: 0.5, intensity: 0.5, variation: 1 }],
  ['dirac', { precision: 3, rate: 2.0 }],
  ['reverb', { roomsize: 0.5, wet: 0.5, dry: 0.5, width: 0.55 }],
]);

const Flow = ({ submit }: any) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [instance, setInstance] = useState<ReactFlowInstance>();
  const [showContextMenu, setShowContextMenu] = useState(false);
  const [contextPosition, setContextPosition] = useState<XYPosition>({
    x: 0,
    y: 0,
  });
  const [currView, setCurrView] = useState<Viewport>({ x: 0, y: 0, zoom: 1 });

  const edgeUpdateSuccessful = useRef(true);
  const currentNode = useRef<Node>();
  const idRef = useRef<any>({
    oscillator: 0,
    envelope: 0,
    value: 0,
    sum: 0,
    multi: 0,
    bezier: 0,
    mix: 0,
    noise: 0,
    filter: 0,
    vibrato: 0,
    dirac: 0,
    reverb: 0,
  });

  const nodeTypes = useMemo(
    () => ({
      oscillator: OscillatorNode,
      envelope: EnvelopeNode,
      value: ValueNode,
      sum: SumNode,
      multi: MultiNode,
      out: OutputNode,
      bezier: BezierNode,
      mix: MixNode,
      noise: NoiseNode,
      filter: FilterNode,
      vibrato: VibratoNode,
      dirac: DiracNode,
      reverb: ReverbNode,
    }),
    []
  );

  // SUBMIT CURRENT FLOW STATE
  const getFlow = useCallback(() => {
    if (instance) {
      const nodesList = instance.getNodes();
      const edgesList = instance.getEdges();

      submit({ nodes: nodesList, edges: edgesList });
    }
  }, [instance, submit]);

  // KEYDOWN EVENT LISTENERS
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

  // ADD NODE
  const addNode = useCallback(
    (nodeType: string, nodePos: XYPosition, view: Viewport, data?: Object) => {
      let nodeData: Object;
      if (data) {
        nodeData = data;
      } else {
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
    [setNodes]
  );

  const onSelectionChange = useCallback(
    ({ nodes, edges }: OnSelectionChangeParams) => {
      nodes.forEach((node: Node) => {
        if (node.selected) currentNode.current = node;
      });
    },
    []
  );

  const removeNode = useCallback(
    (n: Node) => {
      setNodes((nds) => nds.filter((node) => node.id !== n.id));
    },
    [setNodes]
  );

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
    [setEdges]
  );

  const onEdgeUpdateEnd = useCallback(
    (_: any, edge: Edge) => {
      if (!edgeUpdateSuccessful.current) {
        setEdges((eds) => eds.filter((e) => e.id !== edge.id));
      }
    },
    [setEdges]
  );

  const onPaneContextMenu = useCallback((event: any, hotkey?: boolean) => {
    event.preventDefault();
    let viewport_x;
    let viewport_y;
    const boundingBox = event.target.getBoundingClientRect();
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

  const onMoveEnd = useCallback((event: any, view: Viewport) => {
    setCurrView(view);
  }, []);

  // SAVE TO LOCAL STORAGE
  const saveProfile = useCallback(() => {
    if (!instance) throw Error('Cannot find reactFlowInstance.');
    const saveKey = prompt('What would you like to save this profile as?');
    if (!saveKey) return;
    const saveObj = {
      profile: instance.toObject(),
      ids: idRef.current,
    };
    localStorage.setItem(saveKey, JSON.stringify(saveObj));
  }, [instance]);

  // LOAD FROM LOCAL STORAGE
  const restoreProfile = useCallback(
    async (loadKey: string) => {
      if (!loadKey) throw Error('No key provided.');
      console.log(loadKey);
      const loadObj = await JSON.parse(localStorage.getItem(loadKey) || '');
      if (!loadObj) throw Error('getItem() failed or stored value is empty.');
      const { x = 0, y = 0, zoom = 1 } = loadObj.profile.viewport;
      setNodes(loadObj.profile.nodes || []);
      setEdges(loadObj.profile.edges || []);
      setCurrView({ x, y, zoom });
      idRef.current = loadObj.ids;
    },
    [setNodes, setEdges]
  );

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
        onClick={(n: string) => addNode(n, contextPosition, currView)}
      />
      <ControllButtons
        saveProfile={saveProfile}
        instance={instance}
        restoreProfile={restoreProfile}
        getFlow={getFlow}
      />
      <Background />
    </ReactFlow>
  );
};

export default (props: any) => (
  <ReactFlowProvider>
    <Flow submit={props.submit} />
  </ReactFlowProvider>
);
