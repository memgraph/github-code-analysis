import type { NextPage } from "next";
import dynamic from "next/dynamic";


const orgChart = {
    name: 'CEO',
    children: [
      {
        name: 'Manager',
        attributes: {
          department: 'Production',
        },
        children: [
          {
            name: 'Foreman',
            attributes: {
              department: 'Fabrication',
            },
            children: [
              {
                name: 'Worker',
              },
            ],
          },
          {
            name: 'Foreman',
            attributes: {
              department: 'Assembly',
            },
            children: [
              {
                name: 'Worker',
              },
            ],
          },
        ],
      },
    ],
  };


const D3Tree = dynamic(
    () => import("react-d3-tree/lib/Tree"),
    { ssr: false }
)


const test: NextPage = () => {
    return (
        <D3Tree data={orgChart} collapsible={true} zoomable={true}></D3Tree>
    );
}


export default test;