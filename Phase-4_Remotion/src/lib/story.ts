import storyData from '../../public/data/story.json';
import scenePlanData from '../../public/data/scene-plan.json';

export interface SceneItem {
  scene_id: string;
  chapter_id: number;
  chapter_title: string;
  scene_number: number;
  narration: string;
  visual_subject: string;
  visual_environment: string;
  camera_style: string;
  search_keywords: string[];
  on_screen_text: string;
  estimated_duration: number;
  scene_type?: string;
}

export interface ScenePlan {
  project_title: string;
  genre: string;
  format: string;
  target_duration_seconds: number;
  world: {
    company: string;
    facility: string;
    subterranean_level: string;
    systems: string[];
  };
  scenes: SceneItem[];
}

export const getStoryData = () => storyData;
export const getScenePlan = (): ScenePlan => scenePlanData as unknown as ScenePlan;
