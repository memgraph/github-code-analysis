import dynamic from "next/dynamic";


const D3Tree = dynamic(
    () => import("react-d3-tree/lib/Tree"),
    { ssr: false }
)


const FileTree = ({data}: {data: any}) => {
    return (
        <div style={{border: "black 1px solid", borderRadius: "5px", width:"100%", height:"100%"}}>
            <D3Tree data={data}></D3Tree>
        </div>
        
    );
}


export default FileTree;