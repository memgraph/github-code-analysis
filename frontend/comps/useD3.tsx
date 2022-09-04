import { useRef, useEffect } from "react";
import * as d3 from "d3";

const useD3 = (renderGraph: any) => {
    const ref = useRef<any>();

    useEffect(() => {
        renderGraph.funct(d3.select(ref.current));
        renderGraph.funct(d3.select(ref.current));  // For some odd reason the markers disappear if this line is not here

        return () => {};
    }, [renderGraph.graph_data]);

    return ref;
};

export default useD3;