from services.analysis_service import AnalysisService
from models.schemas import Source, SourceType
from datetime import datetime

def run_example(text: str, sources: list[Source]):
    print("\n" + "="*80)
    print(f"Testing text: {text}")
    print("="*80)
    
    analysis_service = AnalysisService()
    result = analysis_service.analyze_text(text, sources)
    
    print(f"\nResult:")
    print(f"Is Fact: {'✅ Yes' if result['is_fact'] else '❌ No'}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nDetailed Explanation:")
    print(result['explanation'])
    
    if result['discrepancies']:
        print("\nDiscrepancies Found:")
        for d in result['discrepancies']:
            print(f"\nClaim: {d.claim}")
            print(f"Contradicting Source: {d.source}")
            print(f"Source Text: {d.source_text}")
            print(f"Similarity Score: {d.similarity:.2%}")

def main():
    # Example 1: Factual statement about COVID-19 vaccines
    covid_text = "COVID-19 vaccines have been shown to be effective in preventing severe illness and hospitalization. The mRNA vaccines work by teaching cells to produce harmless spike proteins."
    covid_sources = [
        Source(
            title="Effectiveness of COVID-19 Vaccines in Preventing Hospitalization",
            authors=["Smith, J.", "Johnson, M."],
            year=2023,
            journal="Journal of Immunology",
            citations=156,
            abstract="Clinical trials and real-world studies demonstrate that COVID-19 vaccines significantly reduce the risk of severe illness and hospitalization.",
            link="https://example.com/study1",
            source_type=SourceType.SCHOLAR
        ),
        Source(
            title="Understanding mRNA COVID-19 Vaccines",
            snippet="mRNA vaccines work by instructing cells to produce a harmless piece of the virus's spike protein, triggering an immune response.",
            link="https://cdc.gov/vaccines",
            source_type=SourceType.GOOGLE
        )
    ]
    run_example(covid_text, covid_sources)

    # Example 2: Misleading statement about climate change
    climate_text = "Global warming is not real because it still snows in winter. The Earth's temperature has always fluctuated naturally."
    climate_sources = [
        Source(
            title="Climate Change: Evidence and Causes",
            authors=["Brown, R.", "Davis, K."],
            year=2022,
            journal="Nature Climate Science",
            citations=289,
            abstract="Multiple lines of scientific evidence show that Earth's climate is warming due to human activities, particularly the emission of greenhouse gases.",
            link="https://example.com/study2",
            source_type=SourceType.SEMANTIC_SCHOLAR
        ),
        Source(
            title="Weather vs Climate: Understanding the Difference",
            snippet="Individual weather events like snow or cold spells do not disprove global warming. Climate refers to long-term patterns over decades.",
            link="https://nasa.gov/climate",
            source_type=SourceType.GOOGLE
        )
    ]
    run_example(climate_text, climate_sources)

    # Example 3: Historical fact
    history_text = "The Great Wall of China was built in the Ming Dynasty and is visible from space."
    history_sources = [
        Source(
            title="Construction History of the Great Wall",
            authors=["Zhang, L."],
            year=2020,
            journal="Archaeological Review",
            citations=45,
            abstract="While parts of the Great Wall date back to earlier dynasties, most of the current structure was indeed built during the Ming Dynasty (1368-1644).",
            link="https://example.com/study3",
            source_type=SourceType.SCHOLAR
        ),
        Source(
            title="Common Myths About the Great Wall",
            snippet="Contrary to popular belief, the Great Wall of China is not visible from space with the naked eye, as confirmed by multiple astronauts.",
            link="https://space.com/greatwall",
            source_type=SourceType.GOOGLE
        )
    ]
    run_example(history_text, history_sources)

if __name__ == "__main__":
    main() 