import { z } from "zod";

export const compositionSchema = z.object({
  creatorName: z.string().default("MOHIT JAIN"),
  phoneNumber: z.string().default("6263879076"),
  professionTitle: z.string().default("HEALTHCARE WEBSITE ARCHITECT"),
  accentColor: z.string().default("#00F2FE"),
});

export type CompositionProps = z.infer<typeof compositionSchema>;
