import Image from "next/image";
import styles from "./page.module.css";
import NavBar from "@/components/navbar";
import { NavigationMenuDemo } from "@/components/navbar";

export default function LandingPage() {
  return (
    <>
      <NavigationMenuDemo></NavigationMenuDemo>
      <main>
        <h4>Arcade Landing Page</h4>
      </main>
    </>
  );
}
