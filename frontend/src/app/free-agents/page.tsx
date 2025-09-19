import FreeAgentsList from "./FreeAgentsList"
import PageWrapper from "../components/PageWrapper";

export default async function FreeAgentsPage() {
    const res = await fetch("http://localhost:3000/api/free-agents")

    return (
        <PageWrapper>
            <FreeAgentsList/>
        </PageWrapper>
    )
}