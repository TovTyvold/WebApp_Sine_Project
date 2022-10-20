import { useCallback, useMemo, useRef, useState } from 'react';
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
  const newNodeYPos = useRef(0);
  const idCount = useRef(1);
  const edgeUpdateSuccessful = useRef(true);
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

  const addNode = useCallback((nodeType: string) => {
    newNodeYPos.current += 50;
    let data = {};
    if (nodeType === 'oscillator') data = { shape: 'sin' };
    setNodes((nds) => {
      return [
        ...nds,
        {
          id: `${nodeType}-${idCount.current++}`,
          position: { x: 5, y: newNodeYPos.current },
          type: nodeType,
          data: data,
          remove: removeNode,
        },
      ];
    });
  }, []);

  const removeNode = (id: string) => {
    setNodes((nds) => nds.filter((node) => node.id !== id));
  };

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

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onEdgeUpdate={onEdgeUpdate}
      onEdgeUpdateStart={onEdgeUpdateStart}
      onEdgeUpdateEnd={onEdgeUpdateEnd}
      onConnect={onConnect}
      nodeTypes={nodeTypes}
      onInit={setInstance}
      fitView>
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
