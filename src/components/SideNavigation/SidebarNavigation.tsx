import './SidebarNavigation.scss';
import React from 'react';

type Props = {
  visible: boolean;
}

const SidebarNavigation = (props: Props) => {
  return (
    <div className={`SidebarNavigation ${props.visible ? "visible" : ""}`}>
      <div>I am the sidebar</div>
    </div>
  );
};

export default SidebarNavigation;
