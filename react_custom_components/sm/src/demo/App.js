/* eslint no-magic-numbers: 0 */
import React, {Component} from 'react';

import { SideMenu } from '../lib';

export default function App() {
  return (
    <div className="App">
      <SideMenu
        items={[
          { id: "Desc", label: "Description" },
          { id: "Pop", label: "Population concernée" },
          { id: "Effets", label: "Effets indésirables" },
          { id: "EM", label: "Erreurs médicamenteuses" },
          { id: "PF", label: "Pays de fabrication" }
        ]}
      />
      <main>
        <div className="Content">
          <h1>Coucou Florent</h1>
          <h2>Ce soir on va faire du code ça va être le fun!</h2>
        </div>
      </main>
    </div>
  );
}
