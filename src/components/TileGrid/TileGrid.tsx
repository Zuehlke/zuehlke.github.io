import './TileGrid.scss';
import React, {ReactChild} from 'react';

type Props = {
  children: ReactChild[]
}

const TileGrid = (props: Props) => {

  const tile = (child: ReactChild, idx: number) => {

    return (
      <div key={idx} className="grid-cell">
        {child}
      </div>
    );
  }

  return (
    <div className="TileGrid">
      <div className="grid">
        {React.Children.map(props.children, (child: ReactChild, idx: number) => tile(child, idx))}
      </div>
    </div>
  );
};

export default TileGrid;
