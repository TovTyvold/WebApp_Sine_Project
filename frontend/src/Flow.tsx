import React, { useCallback, useMemo, useRef, useState } from 'react';
import { ContextMenu } from './components/ContextMenu';
import ReactFlow, {
  ReactFlowProvider,
  Node,
  addEdge,
  updateEdge,
  Background,
  Controls,
  Edge,
  Connection,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './flow-node.css';

import EnvelopeNode from './components/EnvelopeNode';
import OscillatorNode from './components/OscillatorNode';
import OperationNode from './components/OperationNode';
import EffectNode from './components/EffectNode';
import OutputNode from './components/OutputNode';
import ControllButtons from './components/ControlButtons';
import { FlowArrayMutation } from 'typescript';

const initialNodes: Node[] = [
  {
    id: 'output-0',
    type: 'output',
    data: {},
    position: { x: 350, y: 250 },
  },
];

const initialEdges: Edge[] = [];

const Flow = ({ submit }: any) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [instance, setInstance] = useState<any>(null);
  const idCount = useRef(1);
  const edgeUpdateSuccessful = useRef(true);
  const [showContextMenu, setShowContextMenu] = useState(false);
  const [contextPosition, setContextPosition] = useState({ x: 0, y: 0 });
  const [currView, setCurrView] = useState({x:0, y:0, zoom:0.5});
  const [tree, setTree] = useState();

  const nodeTypes = useMemo(
    () => ({
      oscillator: OscillatorNode,
      envelope: EnvelopeNode,
      operation: OperationNode,
      effect: EffectNode,
      output: OutputNode,
    }),
    []
  );

  const createTree = useCallback((nodesList: Node[], edgesList: Edge[]) => {
    let map: any = new Map(
      nodesList.map((o) => [o.id, { ...o, children: [] }])
    );
    for (let { source, target } of edgesList) {
      map.get(target).children.push(map.get(source));
    }
    return map.get('output-0');
  }, []);

  const getFlow = useCallback(() => {
    if (instance) {
      const nodesList = instance.getNodes();
      const edgesList = instance.getEdges();

      //console.log(JSON.stringify(createTree(nodesList, edgesList), null, 2));
      submit(createTree(nodesList, edgesList));
    }
  }, [instance]);



  const addNode = useCallback((nodeType: string, nodePos: any, view: any) => {
    let data = {};
    if (nodeType === 'oscillator') data = { shape: 'sin' };

    const x = (1/view.zoom)*(nodePos.x - view.x)
    const y = (1/view.zoom)*(nodePos.y - view.y)

    const newNode = {
      id: `${nodeType}-${idCount.current++}`,
      position: {x: x, y: y},
      type: nodeType,
      data: data,
    }

    setNodes((nds) => nds.concat(newNode))
    setShowContextMenu(false)
  }, []);

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((edges) => addEdge(params, edges)),
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

  const onPaneContextMenu = useCallback((event: any) => {
    event.preventDefault()

    setShowContextMenu(true)
    const boundingBox = event.target.getBoundingClientRect();
    const viewport_x = event.pageX - boundingBox.left;
    const viewport_y = event.pageY - boundingBox.top;

    setContextPosition({ x: viewport_x, y: viewport_y })
  }, []);

  const onPaneClick = useCallback((event: any) => {
    setShowContextMenu(false)
  }, [])

  const onMoveEnd = useCallback((event: any, view: any) => {
    setCurrView(view)
  }, [])

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onPaneContextMenu={onPaneContextMenu}
      onPaneClick={onPaneClick}
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
      >
      <ContextMenu show={showContextMenu} position={contextPosition} onClick={(e: any) => addNode(e, contextPosition, currView)}/>
      <ControllButtons getFlow={getFlow} addNode={addNode} />
      <Background />
    </ReactFlow>
  );
};

export default ({ submit }: any) => (
  <ReactFlowProvider>
    <Flow submit={submit} />
  </ReactFlowProvider>
);
