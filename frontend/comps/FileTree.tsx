import dynamic from "next/dynamic";
import { Box } from "@mui/material"
import { useRef } from "react";
import styles from '../styles/filetree.module.css';


const D3Tree = dynamic(
    () => import("react-d3-tree/lib/Tree"),
    { ssr: true }
)


const renderNodeWithCustomEvents = ({nodeDatum,
                                        toggleNode,
                                        handleNodeClick
                                    }: {nodeDatum: any, toggleNode: any, handleNodeClick: any}) => (
    <g>
        <foreignObject x="0" height="120px" width={"400px"} y="-60px" onClick={toggleNode}>
            <div
                title={nodeDatum.fullName}
                className={nodeDatum.attributes?.type == "file" ? styles.elemental_node_file : styles.elemental_node }
            >
                <span title={nodeDatum.name} className={styles.graph_text}>{nodeDatum.name}</span>
            </div>
        </foreignObject>
    </g>
);


const FileTree = ({data}: {data: any}) => {
    const initialDepth = useRef(1)

    const handleNodeClick = (nodeDatum: any) => {
        window.alert(
            nodeDatum.children ? "Clicked a branch node" : "Clicked a leaf node."
        );
    };

    /* branchNodeClassName={"nodeEle"} renderCustomNodeElement={(rts) => <NodeElement nodeDatum={rts.nodeDatum} orientation={"horizontal"} toggleNode={rts.toggleNode} onNodeClick={() => {}} />} */

    return (
        <Box sx={{width:"100%", minHeight: "50vh", height: "100%"}}>
            <D3Tree renderCustomNodeElement={(rd3tProps) =>
                renderNodeWithCustomEvents({ ...rd3tProps, handleNodeClick })
            } pathClassFunc={() => styles.path_link} zoom={0.5} pathFunc={"step"} initialDepth={initialDepth.current} orientation={"horizontal"} translate={{x: 400, y: 350}} nodeSize={{ x: 500, y: 80 }} separation={{ siblings: 1, nonSiblings: 1.5 }} shouldCollapseNeighborNodes={true} data={data}></D3Tree>
        </Box>
        
    );
}


export default FileTree;