import logging
import os

from crewai import LLM, Agent, Crew, Process, Task
from crewai_tools import DallETool, WebsiteSearchTool, tool

logger = logging.getLogger("marketing_bot")


class Agents:
    def __init__(self, model: str, api_key: str, temperature: float, top_p: float):
        os.environ["OPENAI_API_KEY"] = api_key
        self.llm = LLM(
            model=model,
            api_key=api_key,
            temperature=temperature,
            top_p=top_p,
        )

    # --------------------------------------------------------------------
    # Individual Agent Definitions
    # --------------------------------------------------------------------

    def StrategyBriefingAgent(self, company_data: dict):
        agent = Agent(
            role="Strategy and Briefing Specialist",
            goal="""
            Create or update the company's marketing briefing and guidelines
            (target audience, tone of voice, core values, main products, communication style, etc.).
            """,
            backstory="""
            You are a marketing specialist whose mission is to synthesize a company's data
            into a coherent marketing strategy document (briefing). This briefing will be
            the foundation for other teams, ensuring that all campaigns and posts
            are aligned with the brand strategy.
            """,
            llm=self.llm,
            max_iter=1,
            cache=False,
            verbose=True,
        )

        task = Task(
            description="""
            You have been provided with the following company data:
            **({company_data})**

            **Please follow these steps to create or update the company's marketing briefing:**

            1. **Analyze** the provided information about the company:
            - History, mission, vision, products/services, intended target audience, personas,
                and desired communication style.

            2. **Identify** the key points that should make up the briefing:
            - Primary and secondary target audience
            - Tone of voice and style of communication
            - Core values and competitive differentiators
            - Main products or services to be promoted
            - Main marketing objectives (awareness, conversions, etc.)

            3. **Structure** a document in **JSON** format that contains:
            - `CompanyName`
            - `targetAudience`
            - `toneOfVoice`
            - `mainProducts`
            - `coreValues`
            - `communicationStyle`
            - `competitiveDifferentiator`
            - `marketingObjectives`
            - *(other relevant fields based on the provided data)*

            4. **Use** a clear chain of thought and reasoning internally to ensure coherence and avoid redundancy.

            5. **Return** the final briefing as a **JSON**. Only output the JSON, without additional explanation.

            Make sure you incorporate the provided information from **'company_data'**
            when building your final JSON.
            """,
            expected_output="""
            The expected output is a JSON object containing the briefing, for example:
            {{
                "CompanyName": "...",
                "targetAudience": "...",
                "toneOfVoice": "...",
                "mainProducts": "...",
                "coreValues": "...",
                "communicationStyle": "...",
                "competitiveDifferentiator": "...",
                "marketingObjectives": "..."
            }}
            """,
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task])

        result = crew.kickoff(inputs={"company_data": company_data})

        return result.raw if result.raw else result.json_dict()

    # --------------------------------------------------------------------
    # Main Workflow for the Agent Chain
    # --------------------------------------------------------------------

    def Agents_Chain(
        self, *, company_strategy_briefing, general_rules, provided_theme=None
    ):

        # --------------------------------------------------------------------
        # Tools Setup
        # --------------------------------------------------------------------

        @tool
        def get_recent_themes():
            """
            Retrieve a list of recently used themes from the database or mock data.
            Returns a list of dictionaries with 'theme', 'date_used', and 'performance'.
            """
            recent_themes = [
                {
                    "theme": "Data Analytics in Retail",
                    "date_used": "2025-01-10",
                    "performance": 5,
                },
                {
                    "theme": "Cloud Migration Tips",
                    "date_used": "2025-01-15",
                    "performance": 7,
                },
            ]
            return recent_themes

        search_tool = WebsiteSearchTool()

        dalle_tool = DallETool(
            model="dall-e-3", size="1024x1024", quality="standard", n=1
        )

        # --------------------------------------------------------------------
        # Agent Definitions
        # --------------------------------------------------------------------

        IdeaGenerationAgent = Agent(
            role="Idea Generation (Brainstorm) Specialist",
            goal="""
                Propose or validate a creative topic (theme) for a marketing post,
                ensuring it aligns with the company's strategy and avoids repetition.
                """,
            backstory="""
                You are a marketing strategist specialized in brainstorming new
                post ideas. You have access to the company's marketing briefing and
                a record of recently used themes.
                """,
            llm=self.llm,
            max_iter=1,
            cache=False,
            verbose=False,
            allow_delegation=False,
            tools=[get_recent_themes, search_tool],
        )

        WritingCopywritingAgent = Agent(
            role="Writing and Copywriting Specialist",
            goal="""
                Utilize the company's strategy briefing and the chosen theme to generate
                high-quality, persuasive, or informative content for social media posts,
                adhering to brand guidelines and optimizing for the chosen platform.
                """,
            backstory="""
                You are an expert in copywriting, specializing in creating engaging content
                for social media platforms. Your objective is to transform a theme and
                strategic inputs into polished and compelling text that resonates with
                the target audience while maintaining the brand's voice.
                """,
            llm=self.llm,
            max_iter=1,
            cache=False,
            verbose=False,
            allow_delegation=False,
        )

        ReviewComplianceAgent = Agent(
            role="Review and Compliance Specialist",
            goal="""
                Ensure the generated text adheres to grammar, spelling, style, and compliance standards.
                Validate content against brand guidelines, ensuring it is error-free, compliant,
                and optimized for communication.
                """,
            backstory="""
                You are a specialist in content review and compliance. Your role is to ensure the text created
                y the copywriting agent is polished, accurate, and aligned with all relevant grammatical and
                compliance rules. You aim to elevate the quality and ensure the text is ready for publication.
                """,
            llm=self.llm,
            max_iter=1,
            cache=False,
            verbose=False,
            allow_delegation=False,
        )

        EngagementOptimizationAgent = Agent(
            role="Engagement Optimization Specialist",
            goal="""
                Optimize the final content by adding hashtags and mentions to increase visibility
                and engagement across social media platforms.
                """,
            backstory="""
                You are a specialist in social media engagement optimization. Your goal is to take the revised content
                and enhance it with popular hashtags and mentions, ensuring it aligns with current trends and maximizes
                its potential reach.
                """,
            llm=self.llm,
            max_iter=1,
            cache=False,
            verbose=False,
            allow_delegation=False,
            tools=[search_tool],
        )

        VisualCreativeGenerationAgent = Agent(
            role="Visual Creative Generation Specialist",
            goal="""
                Generate or suggest visual creatives (images) that align with the chosen theme or text content,
                enhancing the engagement and aesthetic appeal of the post.
                """,
            backstory="""
                You are a visual content specialist, leveraging AI tools like DALL-E to create compelling and relevant
                images for social media posts. Your role is to visually complement the provided theme or text
                to ensure maximum engagement and alignment with the brand's identity.
                """,
            llm=self.llm,
            max_iter=1,
            cache=False,
            verbose=False,
            allow_delegation=False,
            tools=[dalle_tool],
        )

        ManagerAgent = Agent(
            role="Workflow Manager",
            goal="""
                Oversee the execution of all agents within the content creation workflow. Coordinate the sequence of
                tasks to ensure smooth execution, validation, and alignment with the company’s strategic goals.
                Ensure that agents follow the stipulated rules below:
                ({general_rules})
                """,
            backstory="""
                You are responsible for managing the entire content generation pipeline, ensuring all agents complete
                their tasks effectively and in the correct order. While you do not perform tasks directly, you validate
                that the outputs meet the expected standards and facilitate efficient collaboration among agents.
                """,
            llm=self.llm,
            max_iter=1,
            cache=False,
            verbose=False,
            allow_delegation=True,
        )

        # --------------------------------------------------------------------
        # Task Definitions
        # --------------------------------------------------------------------

        IdeaGenerationTask = Task(
            description="""
            **Your instructions:**

            1. If `provided_theme` is **NOT** empty, you should simply return it
            as the final output (no changes). This means the user explicitly
            wants that theme.

            2. If `provided_theme` is empty or None, you must:

            1. Review 'company strategy briefing' to ensure alignment with
                the brand's audience, tone, values, etc.
            2. Call the function tool to see which themes
                were recently used. Avoid exact duplication if possible.
            3. "Use the search tool to find current trending topics related to subjects the company strategy."
            4. Generate a new theme that fits the company's strategy
                and is not repetitive.
            5. Provide a brief description for the new theme
                (2-3 sentences explaining why it's relevant).

            3. Use an internal reasoning approach to ensure coherence.
            Summarize the rationale silently, but return **only** the final output.

            4. The **final output** must be a **JSON** object:
            {{
                theme": "Some Theme Title",
                "description": "Short explanation about the theme...
            }}
            ---

            **Input Data for reference:**

            - **Company Strategy Briefing**:
            ({company_strategy_briefing})

            - **Provided Theme**:
            ({provided_theme})

            **Tools available**:
            - `get_recent_themes()` to fetch recently used themes from the DB.
            - `search_tool()` to search for relevant topics online related to the topics the company covers.

            **Pay Attention to the general rules to be follow:**
            ({general_rules})
            ---
        """,
            expected_output="""
                The expected output is a JSON object containing the theme, for example:
                {{
                "theme": "chosen theme",
                "description": "short description about the topic"
                }}
            """,
            agent=IdeaGenerationAgent,
        )

        WritingCopywritingTask = Task(
            description="""
            **Your instructions:**

            1. **Input Sources:**
            - `company_strategy_briefing`: This provides the audience, tone of voice, and other key brand details.
            - `themeChosen`: The topic validated or proposed by the IdeaGenerationAgent.

            2. **Content Creation Process:**
            - Review the `company_strategy_briefing` to align with the brand's tone, values, and audience.
            - Use the `themeChosen` to craft the following:
                - A headline (short, captivating, and aligned with the platform).
                - The main body of text (persuasive or informative based on the theme).
                - A Call-to-Action (CTA) that encourages engagement (e.g., comments, shares, clicks).
            - Format the text to fit the target platform (e.g., LinkedIn), adhering to character limits and style.

            3. **Internal Reasoning:**
            - Ensure coherence between the theme, brand guidelines, and audience preferences.
            - Prioritize clarity, conciseness, and alignment with the platform's best practices.

            4. **Output Format:**
            The final output must be a **JSON** object:
            {{
                "headline": "Captivating headline here",
                "body": "Main content text here",
                "cta": "Call-to-action text here"
            }}
            ---

            **Input Data for reference:**

            - **Company Strategy Briefing:**
            ({company_strategy_briefing})

            - **Theme Chosen:**
            - the theme returned by Idea Generation Agent.

            **Pay Attention to the general rules to follow:**
            ({general_rules})
            ---

            **Observations:**
            - The text must be clear, concise, and within character limits for the platform.
            - Maintain an engaging and professional tone.
            - Ensure alignment with the company’s values and target audience.
            """,
            expected_output="""
                The expected output is a JSON object containing the generated content, for example:
                {{
                    "headline": "Captivating headline here",
                    "body": "Main content text here",
                    "cta": "Call-to-action text here"
                }}
            """,
            context=[IdeaGenerationTask],
            agent=WritingCopywritingAgent,
        )

        ReviewComplianceTask = Task(
            description="""
            **Your instructions:**

            1. **Input Sources:**
            - `generated_content`: The JSON object containing the headline, body, and CTA produced by the Writing
            and Copywriting Agent.

            2. **Process Overview:**
            - Begin by combining the `headline`, `body`, and `cta` into a unified text format divided by sections
            (e.g., "Headline", "Body", and "CTA" as titles for respective paragraphs).
            - Conduct a thorough review of the combined text, focusing on:
                - Grammar and spelling corrections.
                - Style consistency (aligned with the brand tone from the company strategy briefing).
                - Semantic clarity and precision.
                - Compliance with brand rules (e.g., no exaggerated claims, appropriate language).
                - Adherence to any legal or ethical policies outlined in the `general_rules`.
            - Ensure the text flows logically and maintains a professional tone.

            3. **Internal Validation:**
            - Use a structured reasoning process to ensure that all errors are addressed.
            - If any major compliance or content issues cannot be resolved automatically, indicate the need for
            human review.

            4. **Output Format:**

            The final output must be a **JSON** object containing the revised content in a single key as follows:
            {{
                "revised_content": "..."
            }}

            Attention:

            - The revised text must be returned without any mention of the keys that previously separated them by
            headline, body and cta, the final output must contain only the complete structured text with all this
            content revised with grammatical corrections applying compliance rules (e.g.: no exaggerated promises,
            no offensive language , etc.).

            ---

            **Input Data for reference:**

            - **Generated Content:**
            - the text prepared by Writing and Copywriting Agent.

            - **General Rules:**
            ({general_rules})

            **Observations:**
            - Ensure grammatical and stylistic accuracy.
            - The revised content must align with compliance rules and company guidelines.
            - Keep the language professional and free of errors.
            """,
            expected_output="""
                The expected output is a JSON object containing the revised text, for example:
                {{
                    "revised_content": "main content text here"
                }}
                Attention:

                - The revised text must be returned without any mention of the keys that previously
                separated them by headline, body and cta, the final output must contain only the complete
                structured text with all this content revised with grammatical corrections applying
                compliance rules (e.g.: no exaggerated promises, no offensive language , etc.).
            """,
            context=[WritingCopywritingTask],
            agent=ReviewComplianceAgent,
        )

        EngagementOptimizationTask = Task(
            description="""
            **Your instructions:**

            1. **Input Sources:**
            - `revised_content`: The text content finalized by the ReviewComplianceAgent.

            2. **Engagement Optimization Process:**
            - Analyze the `revised_content` and identify relevant keywords or phrases that align with the topic.
            - Use the `search_tool` to fetch popular hashtags and trends related to these keywords.
            - Create a list of hashtags that are:
                - Relevant to the content.
                - Popular in the target audience's industry or interests.
            - Integrate the hashtags directly into the `revised_content` at the end, following a line break.
            - Optionally, include mentions or tags to increase visibility.

            3. **Output Requirements:**
            - Return the optimized text with hashtags appended at the end.
            - Include a separate list of hashtags as part of the output for future analysis.

            4. **Internal Validation:**
            - Ensure the hashtags are appropriate, non-offensive, and aligned with the brand's identity.
            - Validate the text flow and ensure the hashtags do not disrupt the content's readability.

            5. **Output Format:**
            The final output must be a **JSON** object:
            {{
                "final_content": "Final text with hashtags included",
                "hashtags": ["#ExampleTag1", "#ExampleTag2"]
            }}
            ---

            **Input Data for reference:**

            - **Revised Content:**
            - the text prepared by the Review and Compliance Agent.

            **Tools Available:**
            - `search_tool`: Use this tool to find popular and trending hashtags related to the topic.

            **Observations:**
            - Ensure hashtags are strategically chosen to maximize reach and engagement.
            - Avoid overloading the content with hashtags; limit them to 5-10 highly relevant ones.
            - Align with the brand's values and tone.
            - If the `imageGenerated` is available, ensure the hashtags complement the visual content.

            **Pay Attention to the general rules to be follow:**
            ({general_rules})
            """,
            expected_output="""
                The expected output is a JSON object containing the optimized content and hashtags, for example:
                Attention: All hashtags must be in Brazilian Portuguese (pt-BR).
                {{
                    "final_content": "Final text content here\n\n#Hashtag1 #Hashtag2",
                    "hashtags": ["#Hashtag1", "#Hashtag2"]
                }}
            """,
            context=[ReviewComplianceTask],
            agent=EngagementOptimizationAgent,
        )

        VisualCreativeGenerationTask = Task(
            description="""
            **Your instructions:**

            1. **Input Sources:**
            - `themeChosen`: The validated or proposed theme by the IdeaGenerationAgent.

            2. **Creative Process:**
            - Use the `themeChosen` as the primary input to generate an image using the DALL-E API.
            - Ensure the generated visual aligns with the brand's tone and the message of the theme.

            3. **Output Requirements:**
            - Generate an image and return the URL or binary file for the image.
            - Include metadata about the image:
                - `title`: A brief title for the image.
                - `description`: A short description explaining the relevance of the image to the theme.
                - `url`: If applicable, the URL to access the image.

            4. **Internal Validation:**
            - Ensure the generated image aligns with the company's branding and compliance standards.
            - If the generated image does not fit the theme or quality standards, regenerate or suggest alternatives.

            5. **Output Format:**
            The final output must be a **JSON** object:
            {{
                "image": {{
                    "title": "Image Title",
                    "description": "Short description explaining the image relevance",
                    "url": "https://example.com/image-generated"
                }}
            }}
            ---

            **Input Data for reference:**

            - **Theme Chosen:**
            - the theme returned by Idea Generation Agent.

            **Tools Available:**
            - `dalle_tool`: Use this tool to generate images based on a text prompt.

            **Observations:**
            - Ensure the image enhances the theme's message and adds value to the post.
            - Align with the brand's values and visual identity.
            - Validate compliance with content policies (e.g., avoid offensive or irrelevant visuals).

            **Pay Attention to the general rules to be follow:**
            ({general_rules})
            """,
            expected_output="""
                The expected output is a JSON object containing the generated image details, for example:
                {{
                    "image": {{
                        "title": "Image Title",
                        "description": "Short description explaining the image relevance",
                        "url": "https://example.com/image-generated"
                    }}
                }}
            """,
            context=[IdeaGenerationTask],
            agent=VisualCreativeGenerationAgent,
        )

        ManagerAgentTask = Task(
            description="""Compile the agent responses into a final JSON object""",
            expected_output="""
            - The final output is a JSON object containing the following structure.
            **Attention:**
            - Some of these agents may return more than one piece of information in their final response,
            be careful to only get the specific information requested to be returned in the final object.
            Do not apply any extra information not requested.
            Example:
            {{
                theme: "IdeaGenerationAgent 'theme' response",
                content: "EngagementOptimizationAgent 'final content' text response",
                image_url: "VisualCreativeGenerationAgent 'image URL' response",
            }}
            """,
            context=[
                IdeaGenerationTask,
                EngagementOptimizationTask,
                VisualCreativeGenerationTask,
            ],
            agent=ManagerAgent,
        )

        crew = Crew(
            agents=[
                IdeaGenerationAgent,
                WritingCopywritingAgent,
                ReviewComplianceAgent,
                EngagementOptimizationAgent,
                VisualCreativeGenerationAgent,
            ],
            tasks=[
                IdeaGenerationTask,
                WritingCopywritingTask,
                ReviewComplianceTask,
                EngagementOptimizationTask,
                VisualCreativeGenerationTask,
                ManagerAgentTask,
            ],
            process=Process.hierarchical,
            manager_agent=ManagerAgent,
            manager_llm=self.llm,
            verbose=True,
        )

        result = crew.kickoff(
            inputs={
                "company_strategy_briefing": company_strategy_briefing,
                "general_rules": general_rules,
                "provided_theme": provided_theme or "",
            }
        )

        return result.raw if result.raw else result.json_dict()
