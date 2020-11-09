import './TileGrid.scss';
import React, {ReactNode} from 'react';

type Props = {
  children: ReactNode[]
}

const TileGrid = (props: Props) => {

  const tile = (child: ReactNode) => {
    return (
      <div className="grid-cell">
        <div className="grid-cell-inner">
          <div className="tile">
            {child}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="TileGrid">
      <div className="grid">
        {props.children.map((child: ReactNode) => tile(child))}
      </div>
    </div>
  );
};

export default TileGrid;
