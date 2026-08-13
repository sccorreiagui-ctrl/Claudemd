import { HashRouter, Routes, Route } from "react-router-dom";
import { Shell } from "./components/Shell";
import { Home } from "./pages/Home";
import { Conteudo } from "./pages/Conteudo";
import { Ciclo } from "./pages/Ciclo";
import { Diagnostico } from "./pages/Diagnostico";
import { Simulados } from "./pages/Simulados";
import { Dashboard } from "./pages/Dashboard";

export function App() {
  return (
    <HashRouter>
      <Shell>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/conteudo" element={<Conteudo />} />
          <Route path="/ciclo" element={<Ciclo />} />
          <Route path="/diagnostico" element={<Diagnostico />} />
          <Route path="/simulados" element={<Simulados />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </Shell>
    </HashRouter>
  );
}
